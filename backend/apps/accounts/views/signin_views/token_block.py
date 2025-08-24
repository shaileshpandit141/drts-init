from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class TokenBlockView(APIView):
    """API view for user sign out functionality."""

    def post(self, request: Request) -> Response:
        """Handle user sign out by blacklisting their refresh token."""
        refresh_token = request.data.get("refresh_token", "")

        try:
            # Get and blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Return success response
            return Response(
                data={"detail": "Your session has been terminated."},
                status=status.HTTP_200_OK,
            )
        except TokenError as error:
            raise ValidationError(
                {"refresh_token": ["The provided token is invalid or expired."]}
            ) from error
