from typing import Any, cast

from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from apps.accounts.permissions import IsAccountVerified
from apps.accounts.serializers import UserSerializer
from apps.accounts.models import User


class UserProfileView(APIView):
    """API View for managing authenticated user information."""

    permission_classes = [IsAuthenticated, IsAccountVerified]
    throttle_classes = [UserRateThrottle]
    cache_key = "user_data"

    def get_user(self, request: Request) -> User:
        return cast(User, request.user)

    def get_cache_key(self, request: Request) -> str:
        """Return cache key base on user id."""
        return f"{self.cache_key}_{self.get_user(request).id}"

    def get(self, request: Request) -> Response:
        # Get cached data if avlaible
        user_data: dict[str, Any] | None = cache.get(self.get_cache_key(request))
        if user_data:
            return Response(data=user_data, status=status.HTTP_200_OK)

        serializer = UserSerializer(
            instance=self.get_user(request),
            many=False,
            context={"request": request},
        )

        # Cached user data of 5 minutes
        cache.set(
            self.get_cache_key(request),
            serializer.data,
            timeout=300,
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request: Request) -> Response:
        """Update authenticated user's profile information."""
        serializer = UserSerializer(
            data=request.data,
            instance=self.get_user(request),
            many=False,
            partial=True,
            context={"request": request},
        )

        # Save valid serializer
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        # Delete Cahce Key if profile updated.
        cache.delete(self.get_cache_key(request))

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
