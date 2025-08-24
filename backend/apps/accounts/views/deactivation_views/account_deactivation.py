from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView


class AccountDeactivationView(APIView):
    """API view for deactivating user accounts."""

    permission_classes = [IsAuthenticated]  # noqa: RUF012
    throttle_classes = [UserRateThrottle]  # noqa: RUF012

    def post(self, request: Request) -> Response:
        """Deactivate the authenticated user's account."""
        user = request.user
        password = request.data.get("password", None)

        # Handle if password is blank
        if password is None:
            raise ValidationError({"password": ["This field is required."]})

        # Verify password matches
        if not user.check_password(password):
            raise ValidationError(
                {
                    "password": [
                        "The password you entered is incorrect. Please try again."
                    ]
                }
            )

        # Deactivate the account
        user.is_active = False
        user.save()

        # Return success response
        return Response(
            data={"detail": "Your account has been deactivated."},
            status=status.HTTP_200_OK,
        )
