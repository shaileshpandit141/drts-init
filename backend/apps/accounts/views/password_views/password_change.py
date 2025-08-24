from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from apps.accounts.serializers import PasswordChangeSerializer


class PasswordChangeView(APIView):
    """Changes authenticated user's password."""

    permission_classes = [IsAuthenticated]  # noqa: RUF012
    throttle_classes = [UserRateThrottle]  # noqa: RUF012

    def post(self, request: Request) -> Response:
        """Changes user password after validation."""
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={"request": request},
        )

        # Validating the serializer data
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,  # type: ignore  # noqa: PGH003
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save the new password
        serializer.save()

        # Return success password change response
        return Response(
            data={"detail": "Your password has been changed successfully."},
            status=status.HTTP_200_OK,
        )
