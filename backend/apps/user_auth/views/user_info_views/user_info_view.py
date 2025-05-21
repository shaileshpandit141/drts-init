from rest_core.response import failure_response, success_response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from user_auth.serializers.user_public_serializer import UserPublicSerializer

from apps.user_auth.permissions import IsUserAccountVerified


class UserInfoView(APIView):
    """API View for managing authenticated user information."""

    permission_classes = [IsAuthenticated, IsUserAccountVerified]
    throttle_classes = [UserRateThrottle]

    def get(self, request) -> Response:
        """Retrieve current user"s profile information."""

        # Create user serializer instance
        serializer = UserPublicSerializer(
            instance=request.user,
            many=False,
            context={"request": request},
        )

        # Return success response
        return success_response(
            message="User profile data fetched successfully",
            data=serializer.data,
        )

    def patch(self, request) -> Response:
        """Update authenticated user's profile information."""

        # Create user serializer instance with new data
        serializer = UserPublicSerializer(
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
