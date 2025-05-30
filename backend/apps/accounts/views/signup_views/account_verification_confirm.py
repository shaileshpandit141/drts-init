from accounts.models import User
from accounts.throttling import AuthUserRateThrottle
from limited_time_token_handler import LimitedTimeTokenDecoder
from rest_core.response import failure_response, success_response
from rest_core.views.mixins import ModelObjectMixin
from rest_framework.response import Response
from rest_framework.views import APIView


class AccountVerificationConfirmView(ModelObjectMixin[User], APIView):
    """API View for verifying user accounts via email confirmation."""

    throttle_classes = [AuthUserRateThrottle]
    queryset = User.objects.filter(is_active=True)

    def get(self, request) -> Response:
        """Handle GET request for account verification."""

        # Get token from query parameters
        token = request.query_params.get("token")

        # Call the _verify_token method to handle verification
        return self._verify_token(token)

    def post(self, request) -> Response:
        """Handle POST request for account verification."""

        # Get token from request data
        token = request.data.get("token")

        # Call the _verify_token method to handle verification
        return self._verify_token(token)

    def _verify_token(self, token: str) -> Response:
        """Verify the provided token and activate the user account."""

        # Check if token is provided or not
        if not token:
            return failure_response(
                message="Token is missing",
                errors={"token": ["Please provide a valid verification token."]},
            )

        # Decode the token and get user ID
        decoder = LimitedTimeTokenDecoder(token)
        if not decoder.is_valid():
            return failure_response(
                message="Invalid token",
                errors={"token": ["The verification token is invalid or has expired."]},
            )

        # Decode the token
        data = decoder.decode()

        # Get user by  ID
        user = self.get_object(id=data.get("user_id"))

        # Check if user exists or not
        if user is None:
            return failure_response(
                message="Invalid verification token",
                errors={"token": ["The token is valid but the user does not exist."]},
            )

        # Check if user is already verified
        if getattr(user, "is_verified", False):
            return success_response(
                message="Account Already Verified",
                data={"detail": "This account has already been verified."},
            )

        # Verify the user account
        setattr(user, "is_verified", True)
        user.save()

        # Return success response
        return success_response(
            message="Account verification successful",
            data={"detail": "Your account has been verified successfully."},
        )
