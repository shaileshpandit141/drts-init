from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjValidationError
from djresttoolkit.views.mixins import RetrieveObjectMixin
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from authmint.exceptions import InvalidTokenError

from apps.accounts.models import User
from apps.accounts.throttling import AuthUserRateThrottle
from apps.accounts.tokenmint import password_reset_mint


class PasswordResetConfirmView(RetrieveObjectMixin[User], APIView):
    """API View to handle password reset and confirmation."""

    throttle_classes = [AuthUserRateThrottle]  # noqa: RUF012
    queryset = User.objects.filter(is_active=True)

    def post(self, request: Request) -> Response:
        """Handle POST request to confirm and reset password."""
        token = request.data.get("token", None)
        new_password = request.data.get("new_password", None)

        # Check if token and new password are provided or not
        if token is None:
            raise ValidationError({"token": ["This field is required."]})
        if new_password is None:
            raise ValidationError({"new_password": ["This field is required."]})

        # Call the _reset_password method to handle password reset
        return self._reset_password(token, new_password)

    def _reset_password(self, token: str, new_password: str) -> Response:
        """Handle the password reset password process."""

        try:
            claims = password_reset_mint.validate_token(token=token)
            user = self.get_object(id=claims["ext"]["user_id"])
            if not user:
                raise ValidationError(
                    {"detail": "User not found with the provided token."}
                )

            try:
                validate_password(new_password)
            except DjValidationError as error:
                raise ValidationError({"password": error.messages}) from error

            # Set new password and save it
            user.set_password(new_password)
            user.save()

            # Return success response
            return Response(
                data={"detail": "Your password has been successfully reset."},
                status=status.HTTP_200_OK,
            )
        except InvalidTokenError:
            raise ValidationError({"detail": "Invalid or expired token."})
