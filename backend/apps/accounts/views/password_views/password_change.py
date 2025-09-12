from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from apps.accounts.serializers import PasswordChangeSerializer
from apps.accounts.tasks import send_password_change_email


class PasswordChangeView(APIView):
    """Changes authenticated user's password."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request: Request) -> Response:
        """Changes user password after validation."""
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={"request": request},
        )

        # Validating the serializer data
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save the new password
        user = serializer.save()

        # Send asynchronously email with account activation link
        send_password_change_email.delay(user.email)  # type: ignore[attr-defined]

        # Return success password change response
        return Response(
            data={"detail": "Your password has been changed successfully."},
            status=status.HTTP_200_OK,
        )
