from rest_core.response import failure_response, success_response
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.serializers.signin_serializers import SigninSerializer
from apps.accounts.throttling import AuthUserRateThrottle


class TokenRetriveView(APIView):
    throttle_classes = [AuthUserRateThrottle]
    queryset = User.objects.filter(is_active=True)

    def post(self, request) -> Response:
        """Handle user sign-in and JWT token generation."""
        # Create a signin serializer instance
        serializer = SigninSerializer(data=request.data)

        # Validating the signin serializer
        if not serializer.is_valid():
            return failure_response(
                message="Sign in failed - Invalid credentials.",
                errors=serializer.errors,
            )

        # Get the JWT by calling save method of the serializer
        jwt_tokens = serializer.save()

        # Return the success response with JWT tokens
        return success_response(
            message="Welcome back! You have successfully signed in.",
            data=jwt_tokens,
        )
