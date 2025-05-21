from apps.user_auth.throttles import AuthUserRateThrottle
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from dns_smtp_email_validator import DNSSMTPEmailValidator
from limited_time_token_handler import LimitedTimeTokenGenerator
from rest_core.email_service import Emails, EmailService, Templates
from rest_core.response import failure_response, success_response
from rest_framework.response import Response
from rest_framework.views import APIView
from user_auth.serializers import UserSerializer

User = get_user_model()


class SignupView(APIView):
    """API view for handling user signup functionality"""

    throttle_classes = [AuthUserRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Handle user registration"""

        # Gatting submitted data from request
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        confirm_password = request.data.get("confirm_password", None)
        active_url = request.data.get("active_url", None)

        # Handle if user not include email in payload
        if email is None:
            return failure_response(
                message="Sign up failed - Invalid email",
                errors={"email": ["Please provide a valid email address."]},
            )

        # Handle if user not include password in payload
        if password is None:
            return failure_response(
                message="Sign up failed - Invalid password",
                errors={"password": ["Please provide a valid password."]},
            )

        # Handle if user not include password in payload
        if confirm_password is None:
            return failure_response(
                message="Sign up failed - Invalid confirm password",
                errors={
                    "confirm_password": ["Please provide a valid confirm password."]
                },
            )

        try:
            # Validate password meets requirements
            validate_password(password)
        except ValidationError:
            return failure_response(
                message="Sign up failed - Invalid password",
                errors={"password": ["Password must be at least 8 characters long."]},
            )

        # Check password confirmation matches
        if password != confirm_password:
            return failure_response(
                message="Sign up failed - Password mismatch",
                errors={
                    "confirm_password": ["Passwords do not match. Please try again."]
                },
            )

        # Validate the email is exist in the internet or not
        validator = DNSSMTPEmailValidator(email)
        if not validator.is_valid():
            return failure_response(
                message="Sign up failed - Invalid email domain",
                errors=validator.errors,  # type: ignore
            )

        # Hash the password for secure storage
        hashed_password = make_password(password)

        # Create new user instance
        serializer = UserSerializer(
            data={"email": email},
            context={"hashed_password": hashed_password},
        )

        # Check serialize is valid or not
        if not serializer.is_valid():
            return failure_response(
                message="Sign up failed - Invalid credentials",
                errors=serializer.errors,
            )

        # Save serializer data if it valid
        serializer.save()
        user = serializer.instance

        # Generate verification token and URL
        generator = LimitedTimeTokenGenerator({"user_id": getattr(user, "id")})
        token = generator.generate()
        if token is None:
            return failure_response(
                message="Sign up failed - Token generation failed",
                errors={"detail": "Unable to generate verification token."},
            )

        # Handel email send
        email = EmailService(
            subject="Verify Your Account",
            emails=Emails(
                from_email=None,
                to_emails=[getattr(user, "email", "Unknown")],
            ),
            context={"user": user, "activate_url": f"{active_url}/{token}"},
            templates=Templates(
                text_template="users/verify_account/confirm_message.txt",
                html_template="users/verify_account/confirm_message.html",
            ),
        )

        # Send deactivation confirmation email
        email.send(fallback=False)

        # Return success response object
        return success_response(
            message="Sign up successful",
            data={"detail": "Success! Please check your email to verify your account."},
        )
