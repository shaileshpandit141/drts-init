from django.contrib.auth.password_validation import validate_password
from limited_time_token_handler import LimitedTimeTokenDecoder
from rest_core.response import failure_response, success_response
from rest_core.views.mixins import ModelObjectMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from user_auth.models import User
from user_auth.throttles import AuthUserRateThrottle


class ForgotPasswordConfirmView(ModelObjectMixin[User], APIView):
    """API view for confirming and resetting a forgotten password."""

    throttle_classes = [AuthUserRateThrottle]
    queryset = User.objects.filter(is_active=True)

    def post(self, request) -> Response:
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

            # Get user by id
            user = self.get_object(id=data.get("user_id"))

            # Check if user exists
            if user is None:
                return failure_response(
                    message="User not found",
                    errors={"detail": "User not found with the provided token."},
                )

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
