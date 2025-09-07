from djresttoolkit.views.mixins import RetrieveObjectMixin
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.tasks import send_password_reset_email
from apps.accounts.throttling import AuthRateThrottle
from apps.accounts.tokenmint import password_reset_mint


class PasswordResetView(RetrieveObjectMixin[User], APIView):
    """API View to hansle password reset."""

    throttle_classes = [AuthRateThrottle]  # noqa: RUF012
    queryset = User.objects.filter(is_active=True)

    def post(self, request: Request) -> Response:
        """Process reset password request and send reset email."""
        email = request.data.get("email")
        reset_confirm_uri = request.data.get("reset_confirm_uri", None)

        # Get user by email
        user = self.get_object(email=email)

        # Check provided email is exists or not
        if user is None:
            raise ValidationError({"email": ["Email address cannot be blank."]})

        # Process request for verified users
        if getattr(user, "is_verified", False):
            # Generate password reset token
            token = password_reset_mint.generate_token(
                subject=f"{user.id}",
                extra_claims={"user_id": user.id},
            )

            # Send asynchronously email with account activation link
            send_password_reset_email.delay(  # type: ignore[attr-defined]
                user.email,
                f"{reset_confirm_uri}/{token}",
            )

            # Return success response
            return Response(
                data={"detail": "Please check your inbox for the Forgot password."},
                status=status.HTTP_200_OK,
            )
        # Return failure response
        return Response(
            data={
                "detail": "You must verify your account to access this resource.",
                "code": "account_not_varified",
            },
            status=status.HTTP_403_FORBIDDEN,
        )
