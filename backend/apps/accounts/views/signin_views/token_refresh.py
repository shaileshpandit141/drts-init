from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class TokenRefreshView(APIView):
    """Custom token refresh view for handling JWT token refresh operations."""

    throttle_classes = [UserRateThrottle]

    def post(self, request: Request) -> Response:
        """Handle token refresh POST requests."""
        refresh_token = request.data.get("refresh_token", "")
        if refresh_token is None:
            raise ValidationError({"refresh_token": ["This field is required."]})

        try:
            jwt_tokens = RefreshToken(refresh_token)
            return Response(
                data={"access_token": str(jwt_tokens.access_token)},
                status=status.HTTP_200_OK,
            )
        except (TokenError, InvalidToken) as error:
            raise ValidationError(
                {"refresh_token": ["The provided token is invalid or expired."]}
            ) from error
