from django.conf import settings
from limited_time_token_handler import LimitedTimeTokenGenerator
from rest_core.email_service import Emails, EmailService, Templates
from rest_core.response import failure_response, success_response
from rest_core.views.mixins import ModelObjectMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from user_auth.models import User
from user_auth.throttles import AuthUserRateThrottle


class ForgotPasswordView(ModelObjectMixin[User], APIView):
    """API endpoint for handling forgot password functionality."""

    throttle_classes = [AuthUserRateThrottle]
    queryset = User.objects.filter(is_active=True)

    def post(self, request) -> Response:
        """Process forgot password request and send reset email."""

        # Get email from request
        email = request.data.get("emial", "")

        # Get user by email
        user = self.get_object(email=email)

        # Check provided email is exists or not
        if user is None:
            return failure_response(
                message="Account is not found with the given credentials.",
                errors={"email": ["No account exists with this email address."]},
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

            # Make activation url as for frontend
            active_url = f"{settings.FRONTEND_URL}/auth/forgot-password-confirm/{token}"

            # Handel email send
            email = EmailService(
                subject="Password Reset Request",
                emails=Emails(
                    from_email=None,
                    to_emails=[user.email],
                ),
                context={"user": user, "active_url": active_url},
                templates=Templates(
                    text_template="users/forgot_password/confirm_message.txt",
                    html_template="users/forgot_password/confirm_message.html",
                ),
            )

            # Send deactivation confirmation email
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
