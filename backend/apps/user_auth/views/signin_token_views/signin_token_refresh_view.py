from rest_core.response import failure_response, success_response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class SigninTokenRefreshView(APIView):
    """Custom token refresh view for handling JWT token refresh operations."""

    def post(self, request, *args, **kwargs) -> Response:
        """Handle token refresh POST requests."""

        # Get refresh token from request
        refresh_token = request.data.get("refresh_token", None)

        # Validate the refresh_token is empty or not
        if refresh_token is None:
            return failure_response(
                message="Failed to refresh token - refresh token is missing",
                errors={"refresh_token": ["Refresh token field cannot be empty"]},
            )

        # Handle Token refresh logic
        try:
            # Create a new refresh token object
            jwt_tokens = RefreshToken(refresh_token)
            return success_response(
                message="Access token refreshed successfully",
                data={"access_token": str(jwt_tokens.access_token)},
            )
        except (TokenError, InvalidToken):
            # Return failure response
            return failure_response(
                message="Token refresh failed - invalid or expired refresh token provided",
                errors={
                    "refresh_token": ["Invalid or expired refresh token provided."]
                },
            )
