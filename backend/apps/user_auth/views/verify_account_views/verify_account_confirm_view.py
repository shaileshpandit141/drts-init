from django.contrib.auth import get_user_model
from limited_time_token_handler import LimitedTimeTokenDecoder, TokenError
from rest_core.response import failure_response, success_response
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user_auth.throttles import AuthUserRateThrottle

User = get_user_model()


class VerifyAccountConfirmView(APIView):
    """API View for verifying user accounts via email confirmation."""

    throttle_classes = [AuthUserRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Handle POST request for email verification"""

        # Validate required fields
        token = request.data.get("token", None)

        # Validate the blank token
        if token is None:
            return failure_response(
                message="Token is missing",
                errors={
                    "token": [
                        "Token field is required. Please provide a valid verification token."
                    ]
                },
            )

        try:
            # Decode verification token
            decoder = LimitedTimeTokenDecoder(token)
            if not decoder.is_valid():
                raise TokenError("The verification token is invalid or has expired.")

            # Token decoding
            data = decoder.decode()
            user = User.objects.get(id=data.get("user_id"))

            # Check if already verified
            if getattr(user, "is_verified", False):
                return success_response(
                    message="Account Already Verified",
                    data={"detail": "This account has already been verified."},
                )

            # Update verification status
            setattr(user, "is_verified", True)
            user.save()

            # Return success response
            return success_response(
                message="Account verification successful",
                data={"detail": "Your account has been verified successfully."},
            )

        except (ValueError, TokenError):
            return failure_response(
                message="Invalid verification token",
                errors={
                    "token": [
                        "The provided verification token is invalid or has expired."
                    ]
                },
            )
