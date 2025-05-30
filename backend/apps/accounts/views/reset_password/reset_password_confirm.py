from accounts.models import User
from accounts.throttling import AuthUserRateThrottle
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from limited_time_token_handler import LimitedTimeTokenDecoder
from rest_core.response import failure_response, success_response
from rest_core.views.mixins import ModelObjectMixin
from rest_framework.response import Response
from rest_framework.views import APIView


class ResetPasswordConfirmView(ModelObjectMixin[User], APIView):
    """API View to handle password reset and confirmation."""

    throttle_classes = [AuthUserRateThrottle]
    queryset = User.objects.filter(is_active=True)

    def post(self, request) -> Response:
        """Handle POST request to confirm and reset password."""

        # Get token and new password from request
        token = request.data.get("token", None)
        new_password = request.data.get("new_password", None)

        # Check if token is provided or not
        if token is None:
            return failure_response(
                message="Token is required.",
                errors={"token": ["Token cannot be blank."]},
            )

        # Check if new password is provided or not
        if new_password is None:
            return failure_response(
                message="New password is required.",
                errors={"new_password": ["New password cannot be blank."]},
            )

        # Call the _reset_password method to handle password reset
        return self._reset_password(token, new_password)

    def _reset_password(self, token: str, new_password: str) -> Response:
        """Handle the password reset password process."""

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
        payload = decorder.decode()

        # Get user by id
        user = self.get_object(id=payload.get("user_id"))

        # Check if user exists
        if user is None:
            return failure_response(
                message="User not found with the provided token.",
                errors={"detail": "User not found with the provided token."},
            )

        # Validate and set new password
        try:
            validate_password(new_password)
        except ValidationError as error:
            return failure_response(
                message="Password validation error.",
                errors={"password": error.messages},
            )

        # Set new password and save user
        user.set_password(new_password)
        user.save()

        # Return success response
        return success_response(
            message="Your password has been reset successfully.",
            data={"detail": "Your password has been successfully reset."},
        )
