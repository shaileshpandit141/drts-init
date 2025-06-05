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

    def get(self, request) -> Response:
        """Retrieve current user"s profile information."""

        # Define cache key as for user
        cache_key = f"user_data_{request.user.id}"

        # Get cached data if avlaible
        user_data: dict[str, Any] | None = cache.get(cache_key)
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
        cache.set(cache_key, serializer.data, timeout=300)

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

        # Return updated data
        return success_response(
            message="User profile has been updated successfully",
            data=serializer.data,
        )
