from accounts.models import User
from accounts.throttling import AuthUserRateThrottle
from limited_time_token_handler import LimitedTimeTokenGenerator
from rest_core.email_service import Emails, EmailService, Templates
from rest_core.response import failure_response, success_response
from rest_core.views.mixins import ModelObjectMixin
from rest_framework.response import Response
from rest_framework.views import APIView


class PasswordResetView(ModelObjectMixin[User], APIView):
    """API View to hansle password reset."""

    throttle_classes = [AuthUserRateThrottle]
    queryset = User.objects.filter(is_active=True)

    def post(self, request) -> Response:
        """Process reset password request and send reset email."""

        # Get email from request
        email = request.data.get("email")
        reset_confirm_uri = request.data.get("reset_confirm_uri", None)

        # Get user by email
        user = self.get_object(email=email)

        # Check provided email is exists or not
        if user is None:
            return failure_response(
                message="Invalid email address.",
                errors={"email": ["Email address cannot be blank."]},
            )

        # Process request for verified users
        if getattr(user, "is_verified", False):
            # Generate password reset token
            generator = LimitedTimeTokenGenerator({"user_id": getattr(user, "id")})
            token = generator.generate()
            if token is None:
                return failure_response(
                    message="Failed to generate token. Please try again later.",
                    errors={
                        "detail": "Failed to generate token. Please try again later."
                    },
                )

            # Creating the Email Service instance
            email = EmailService(
                subject="Password Reset Request",
                emails=Emails(
                    from_email=None,
                    to_emails=[user.email],
                ),
                context={"user": user, "active_url": f"{reset_confirm_uri}/{token}"},
                templates=Templates(
                    text_template="accounts/password_reset/confirm_message.txt",
                    html_template="accounts/password_reset/confirm_message.html",
                ),
            )

            # Send reset password email
            email.send(fallback=False)

            # Return success response
            return success_response(
                message="Forgot password email sent.",
                data={"detail": "Please check your inbox for the Forgot password."},
            )
        else:
            # Return failure response
            return failure_response(
                message="Please verify your account to continue.",
                errors={
                    "detail": "You must verify your account to access this resource.",
                    "code": "account_not_varified",
                },
            )
