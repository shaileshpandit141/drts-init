from django.contrib.auth import get_user_model
from limited_time_token_handler import LimitedTimeTokenGenerator
from rest_core.email_service import Emails, EmailService, Templates
from rest_core.response import failure_response, success_response
from rest_core.views.mixins import ModelObjectMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user_auth.throttles import AuthUserRateThrottle

User = get_user_model()


class VerifyAccountView(ModelObjectMixin[User], APIView):
    """API View for handling account verification."""

    throttle_classes = [AuthUserRateThrottle]
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs) -> Response:
        """Process a request to resend an account verification email."""

        # Gatting submitted data from request
        email = request.data.get("email", None)
        active_url = request.data.get("active_url", None)

        # Handle if user not include email in payload
        if email is None:
            return failure_response(
                message="Email is required",
                errors={"email": ["Please provide an email address."]},
            )

        # Get user by email
        user = self.get_object(email=email)

        # Check if user is None
        if user is None:
            return failure_response(
                message="Account not found",
                errors={"email": ["No account exists with this email address."]},
            )

        # Check if user is verified or not
        if not getattr(user, "is_verified", False):
            # Generate verification token and URL
            generator = LimitedTimeTokenGenerator({"user_id": getattr(user, "id")})
            token = generator.generate()
            if token is None:
                return failure_response(
                    message="Verification token generation failed",
                    errors={"detail": "Unable to generate verification token."},
                )

            # Handel email send
            email = EmailService(
                subject="Account Verification Request",
                emails=Emails(
                    from_email=None,
                    to_emails=[user.email],
                ),
                context={"user": user, "activate_url": f"{active_url}/{token}"},
                templates=Templates(
                    text_template="users/verify_account/confirm_message.txt",
                    html_template="users/verify_account/confirm_message.html",
                ),
            )

            # Send verification email
            email.send(fallback=False)

            # Return success response
            return success_response(
                message="Verification email sent",
                data={
                    "detail": "We've sent a verification link to your email address."
                },
            )
        else:
            # Return already verified success response
            return success_response(
                message="Account Already Verified",
                data={"detail": "Your account has already been verified."},
            )
