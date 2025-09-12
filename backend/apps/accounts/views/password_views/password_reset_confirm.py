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
from apps.accounts.throttling import AuthRateThrottle
from apps.accounts.tokenmint import password_reset_mint
from apps.accounts.serializers import PasswordResetConfirmSerializer


class PasswordResetConfirmView(RetrieveObjectMixin[User], APIView):
    """API View to handle password reset and confirmation."""

    throttle_classes = [AuthRateThrottle]
    queryset = User.objects.filter(is_active=True)

    def post(self, request: Request) -> Response:
        """Handle POST request to confirm and reset password."""
        serializer = PasswordResetConfirmSerializer(
            data=request.data,
            many=False,
        )
        return self._reset_password(
            serializer.validated_data["token"],
            serializer.validated_data["new_password"],
        )

    def not_found_detail(self) -> dict[str, str] | str:
        return "User not found with the provided token."

    def _reset_password(self, token: str, new_password: str) -> Response:
        """Handle the password reset password process."""

        try:
            claims = password_reset_mint.validate_token(token=token)
            user = self.get_object(id=claims["ext"]["user_id"])

            # Validate and set new password
            validate_password(new_password)
            user.set_password(new_password)
            user.save()

            # Return success response
            return Response(
                data={"detail": "Your password has been successfully reset"},
                status=status.HTTP_200_OK,
            )
        except (InvalidTokenError, DjValidationError) as error:
            msg: str = "Invalid or expired token."

            if isinstance(error, DjValidationError):
                msg = "Please provide valid password"

            raise ValidationError({"detail": msg})
