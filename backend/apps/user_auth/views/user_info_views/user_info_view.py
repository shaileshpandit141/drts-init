from django.contrib.auth import get_user_model
from rest_core.response import failure_response, success_response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from user_auth.serializers import UserSerializer

from apps.user_auth.permissions import IsUserAccountVerified

User = get_user_model()


class UserInfoView(APIView):
    """API View for managing authenticated user information."""

    permission_classes = [IsAuthenticated, IsUserAccountVerified]
    throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **kwargs) -> Response:
        """Retrieve current user"s profile information."""

        # Get user from request
        user = request.user

        # Serilizer user data
        serializer = UserSerializer(
            instance=user, many=False, context={"request": request}
        )

        # Return success response
        return success_response(
            message="User profile data fetched successfully",
            data=serializer.data,
        )

    def patch(self, request, *args, **kwargs) -> Response:
        """Update authenticated user's profile information."""

        # Create user serializer instance with new data
        serializer = UserSerializer(
            data=request.data,
            instance=request.user,
            many=False,
            partial=True,
        )

        # Check if serializer is valid or not
        if not serializer.is_valid():
            return failure_response(
                message="Unable to update profile - invalid data provided",
                errors=serializer.errors,
            )

        # Save valid serializer data
        serializer.save()

        # Return saved data
        return success_response(
            message="User profile has been updated successfully", data=serializer.data
        )
