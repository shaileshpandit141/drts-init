from djresttoolkit.urls import build_absolute_uri
from djresttoolkit.views.mixins import RetrieveObjectMixin
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.tasks import send_account_verification_email
from apps.accounts.throttling import AuthUserRateThrottle
from apps.accounts.tokenmint import account_verification_mint


class AccountVerificationView(RetrieveObjectMixin[User], APIView):
    """API View for handling account verification."""

    throttle_classes = [AuthUserRateThrottle]  # noqa: RUF012
    queryset = User.objects.filter(is_active=True)

    def post(self, request: Request) -> Response:
        """Process a request to resend an account verification email."""
        email = request.data.get("email", None)
        verification_uri = request.data.get("verification_uri", None)

        # Handle if user not include email in payload
        if email is None:
            raise ValidationError({"email": ["This field is required."]})

        # Get user by email
        user = self.get_object(email=email)

        # Check if user is None
        if user is None:
            raise ValidationError(
                {"email": ["No account exists with this email address."]}
            )

        # Check if user is verified or not
        if not getattr(user, "is_verified", False):
            # Generate verification token
            token = account_verification_mint.generate_token(
                subject=f"{user.id}",
                extra_claims={"user_id": user.id},
            )

            # Get the absolute URL for verification
            if verification_uri is None:
                activate_url = build_absolute_uri(
                    request=request,
                    url_name="accounts:account-verification-confirm",
                    query_params={"token": token},
                )
            else:
                activate_url = f"{verification_uri}/{token}"

            # Send asynchronously email with account verification link
            send_account_verification_email.delay(user.email, activate_url)  # type: ignore[attr-defined]

            # Return success response
            return Response(
                {
                    "detail": "We've sent a verification link to your email address.",
                },
                status=status.HTTP_200_OK,
            )
        # Return already verified success response
        return Response(
            {"detail": "Your account has already been verified."},
            status=status.HTTP_200_OK,
        )
