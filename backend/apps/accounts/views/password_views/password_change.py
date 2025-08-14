from rest_core.email_service import Emails, EmailService, Templates
from rest_core.response import failure_response, success_response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from apps.accounts.serializers.password_serializers import PasswordChangeSerializer


class PasswordChangeView(APIView):
    """Changes authenticated user's password."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request) -> Response:
        """Changes user password after validation."""
        # Creating the serializer instance
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={"request": request},
        )

        # Validating the serializer data
        if not serializer.is_valid():
            return failure_response(
                message="Invalid Password Change Request",
                errors=serializer.errors,
            )

        # Save the new password
        message = serializer.save()

        # Creating the Email Service instance
        email = EmailService(
            subject="Password Change Notification",
            emails=Emails(
                from_email=None,
                to_emails=[request.user.email],
            ),
            context={"user": request.user},
            templates=Templates(
                text_template="accounts/password_change/success_message.txt",
                html_template="accounts/password_change/success_message.html",
            ),
        )

        # Send password changed success email
        email.send(fallback=False)

        # Return success password change response
        return success_response(
            message="Password Changed Successfully",
            data=message,
        )
