from djresttoolkit.views.mixins import RetrieveObjectMixin
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.throttling import AuthUserRateThrottle
from apps.accounts.tokenmint import account_verification_mint
from authmint.exceptions import InvalidTokenError


class AccountActivationConfirmView(RetrieveObjectMixin[User], APIView):
    """API View for verifying user accounts via email confirmation."""

    throttle_classes = [AuthUserRateThrottle]  # noqa: RUF012
    queryset = User.objects.filter(is_active=True)

    def get(self, request: Request) -> Response:
        """Handle GET request for account verification."""
        token = request.query_params.get("token")
        return self._verify_token(token)

    def post(self, request: Request) -> Response:
        """Handle POST request for account verification."""
        token = request.data.get("token")
        return self._verify_token(token)

    def _verify_token(self, token: str | None) -> Response:
        """Verify the provided token and activate the user account."""
        if token is None:
            raise ValidationError(
                {"detail": "The token is invalid or has expired."},
                code="required",
            )

        # Decode token and get user ID
        try:
            claims = account_verification_mint.validate_token(
                token=token,
            )

            user = self.get_object(id=claims["user_id"])
            if not user:
                raise ValidationError(
                    {"detail": "The token is valid but the user does not exist."},
                    code="not_found",
                )

            # Check if user is already verified or not
            if getattr(user, "is_verified", False):
                raise ValidationError(
                    {"detail": "This account has already been verified."},
                    code="already_verified",
                )

            # Verify the user account
            user.is_verified = True
            user.save()

            # Return success response
            return Response(
                data={"detail": "Your account has been verified successfully."},
                status=status.HTTP_200_OK,
            )
        except InvalidTokenError:
            raise ValidationError(
                {"detail": "The token is invalid or has expired."},
                code="invalid",
            )
