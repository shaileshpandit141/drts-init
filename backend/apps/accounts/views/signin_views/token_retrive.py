from collections.abc import Sequence

from rest_core.response import failure_response, success_response
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import BaseThrottle
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.serializers.signin_serializers import SigninSerializer
from apps.accounts.throttling import AuthUserRateThrottle


class TokenRetriveView(APIView):
    """Handle token retrival."""

    throttle_classes: Sequence[type[BaseThrottle]] = [
        AuthUserRateThrottle,
    ]
    queryset = User.objects.filter(is_active=True)

    def post(self, request: Request) -> Response:
        """Handle user sign-in and JWT token generation."""
        # Create a signin serializer instance
        serializer = SigninSerializer(data=request.data)

        # Validating the signin serializer
        if not serializer.is_valid():
            return failure_response(
                message="Sign in failed - Invalid credentials.",
                errors=serializer.errors,  # type: ignore[]
            )

        # Calling save method and get user
        user = serializer.save()

        # Return the success response with JWT tokens
        return success_response(
            message="Welcome back! You have successfully signed in.",
            data=user.get_jwt_tokens(),
        )
