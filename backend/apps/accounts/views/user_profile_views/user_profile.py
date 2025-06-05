from typing import Any

from accounts.permissions import IsUserAccountVerified
from accounts.serializers.user_serializers import UserSerializer
from django.core.cache import cache
from rest_core.response import failure_response, success_response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView


class UserProfileView(APIView):
    """API View for managing authenticated user information."""

    permission_classes = [IsAuthenticated, IsUserAccountVerified]
    throttle_classes = [UserRateThrottle]
    cache_key = "user_data"

    def get_cache_key(self, request) -> str:
        "Return cache key base on user id"
        return f"{self.cache_key}_{request.user.id}"

    def get(self, request) -> Response:
        """Retrieve current user"s profile information."""

        # Get cached data if avlaible
        user_data: dict[str, Any] | None = cache.get(self.get_cache_key(request))
        if user_data:
            return success_response(
                message="User profile fetched successfully",
                data=user_data,
            )

        # Create user serializer instance
        serializer = UserSerializer(
            instance=request.user,
            many=False,
            context={"request": request},
        )

        # Cached user data of 5 minutes
        cache.set(
            self.get_cache_key(request),
            serializer.data,
            timeout=300,
        )

        # Return success response
        return success_response(
            message="User profile fetched successfully",
            data=serializer.data,
        )

    def patch(self, request) -> Response:
        """Update authenticated user's profile information."""

        # Create user serializer instance with new data
        serializer = UserSerializer(
            data=request.data,
            instance=request.user,
            many=False,
            partial=True,
            context={"request": request},
        )

        # Check if serializer is valid or not
        if not serializer.is_valid():
            return failure_response(
                message="User credentials update failed - invalid data provided",
                errors=serializer.errors,
            )

        # Save valid serializer data
        serializer.save()

        # Delete Cahce Key if profile updated.
        cache.delete(self.get_cache_key(request))

        # Return updated data
        return success_response(
            message="User profile has been updated successfully",
            data=serializer.data,
        )
