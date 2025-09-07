from typing import Any

from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from apps.accounts.permissions import IsAccountVerified
from apps.accounts.serializers.user_serializers import UserSerializer


class UserProfileView(APIView):
    """API View for managing authenticated user information."""

    permission_classes = [IsAuthenticated, IsAccountVerified]  # noqa: RUF012
    throttle_classes = [UserRateThrottle]  # noqa: RUF012
    cache_key = "user_data"

    def get_cache_key(self, request: Request) -> str:
        """Return cache key base on user id."""
        return f"{self.cache_key}_{request.user.id}"  # type: ignore  # noqa: PGH003

    def get(self, request: Request) -> Response:
        """Retrieve current user"s profile information."""
        # Get cached data if avlaible
        user_data: dict[str, Any] | None = cache.get(self.get_cache_key(request))
        if user_data:
            return Response(data=user_data, status=status.HTTP_200_OK)

        # Create user serializer instance
        serializer = UserSerializer(
            instance=request.user,  # type: ignore  # noqa: PGH003
            many=False,
            context={"request": request},
        )

        # Cached user data of 5 minutes
        cache.set(
            self.get_cache_key(request),
            serializer.data,  # type: ignore  # noqa: PGH003
            timeout=300,
        )

        # Return success response
        return Response(data=serializer.data, status=status.HTTP_200_OK)  # type: ignore  # noqa: PGH003

    def patch(self, request: Request) -> Response:
        """Update authenticated user's profile information."""
        serializer = UserSerializer(
            data=request.data,
            instance=request.user,  # type: ignore  # noqa: PGH003
            many=False,
            partial=True,
            context={"request": request},
        )

        # Check if serializer is valid or not
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,  # type: ignore  # noqa: PGH003
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save valid serializer data
        serializer.save()

        # Delete Cahce Key if profile updated.
        cache.delete(self.get_cache_key(request))

        # Return updated data
        return Response(
            data=serializer.data,  # type: ignore  # noqa: PGH003
            status=status.HTTP_200_OK,
        )
