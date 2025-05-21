from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from limited_time_token_handler import LimitedTimeTokenDecoder
from rest_core.response import failure_response, success_response
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user_auth.throttles import AuthUserRateThrottle

User = get_user_model()


class ForgotPasswordConfirmView(APIView):
    """API view for confirming and resetting a forgotten password."""

    throttle_classes = [AuthUserRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Handle POST request to confirm and reset password."""

        # Get token and new password from request
        token = request.data.get("token", "")
        new_password = request.data.get("new_password", "")

        try:
            # Decode token and get user id
            decorder = LimitedTimeTokenDecoder(token)
            if not decorder.is_valid():
                return failure_response(
                    message="The password reset token has expired or is invalid.",
                    errors={
                        "token": [
                            "Invalid or expired token. Please request a new password reset."
                        ]
                    },
                )

            # Decodeing token
            data = decorder.decode()
            user = User.objects.get(id=data.get("user_id"))

            # Validate and set new password
            validate_password(new_password)
            user.set_password(new_password)
            user.save()

            # Return success response
            return success_response(
                message="Password successfully reset",
                data={"detail": "Your password has been successfully reset."},
            )
        except Exception:
            return failure_response(
                message="An error occurred while resetting your password",
                errors={"detail": "Something is wrong. Please try again."},
            )
