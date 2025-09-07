from djresttoolkit.urls import build_absolute_uri
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.serializers.signup_serializers import SignupSerializer
from apps.accounts.tasks import send_account_verification_email
from apps.accounts.tokenmint import account_verification_mint
from apps.accounts.throttling import AuthUserRateThrottle


class SignupView(APIView):
    """API view for handling user signup functionality."""

    throttle_classes = [AuthUserRateThrottle]

    def post(self, request: Request) -> Response:
        """Handle user registration."""
        # Get the verification URL from the request data
        verification_uri = request.data.get("verification_uri", None)

        # Create an instance of the SignupSerializer
        serializer = SignupSerializer(data=request.data)

        # Validate the serializer data
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,  # type: ignore  # noqa: PGH003
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save serializer data if it valid
        serializer.save()
        user = serializer.instance  # type: ignore  # noqa: PGH003

        if not user:
            raise ValidationError({"detail": "Opps! Something is wrong!"})

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

        # Return success response object
        return Response(
            data={"detail": "Success! Please check your email to verify your account."},
            status=status.HTTP_201_CREATED,
        )
