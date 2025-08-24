from collections.abc import Sequence

from rest_framework import status
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
        serializer = SigninSerializer(data=request.data)

        # Validating the signin serializer
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,  # type: ignore[]
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Calling save method and get user
        user = serializer.save()

        # Return the success response with JWT tokens
        return Response(
            data=user.get_jwt_tokens(),
            status=status.HTTP_200_OK,
        )
