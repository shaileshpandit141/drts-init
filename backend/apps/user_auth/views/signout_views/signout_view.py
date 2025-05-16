from rest_core.response import failure_response, success_response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class SignoutView(APIView):
    """API view for user sign out functionality."""

    def post(self, request, *args, **kwargs) -> Response:
        """Handle user sign out by blacklisting their refresh token."""

        # Get required data from response
        refresh_token = request.data.get("refresh_token", "")

        try:
            # Get and blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Return success response
            return success_response(
                message="You have been successfully signed out.",
                data={"detail": "Your session has been terminated."},
            )
        except TokenError:
            # Return failure response
            return failure_response(
                message="Invalid refresh token.",
                errors={"detail": "The provided token is invalid or expired."},
            )
