from limited_time_token_handler import LimitedTimeTokenGenerator
from rest_core.build_absolute_uri import build_absolute_uri
from rest_core.email_service import Emails, EmailService, Templates
from rest_core.response import failure_response, success_response
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.apps.user_auth.serializers.signup_serializer import SignupSerializer
from user_auth.throttles import AuthUserRateThrottle


class SignupView(APIView):
    """API view for handling user signup functionality"""

    throttle_classes = [AuthUserRateThrottle]

    def post(self, request) -> Response:
        """Handle user registration"""

        # Get the verification URL from the request data
        verification_uri = request.data.get("verification_uri", None)

        # Create an instance of the SignupSerializer
        serializer = SignupSerializer(data=request.data)

        # Validate the serializer data
        if not serializer.is_valid():
            return failure_response(
                message="Sign up failed - Invalid credentials", errors=serializer.errors
            )

        # Save serializer data if it valid
        serializer.save()
        user = serializer.instance

        # Generate verification token and URL
        generator = LimitedTimeTokenGenerator({"user_id": getattr(user, "id")})
        token = generator.generate()
        if token is None:
            return success_response(
                message="Sign up success - Token generation failed.",
                data={
                    "detail": "Sign up success but token generation failed.",
                    "token": "You need to generate an account verification token and verify it.",
                },
            )

        # Get the absolute URL for verification
        if verification_uri is None:
            activate_url = build_absolute_uri(
                request=request,
                view_name="user_auth:verify-account-confirm",
                query_params={"token": token},
            )
        else:
            activate_url = f"{verification_uri}/{token}"

        # Creating the Email Service instance
        email = EmailService(
            subject="Verify Your Account",
            emails=Emails(
                from_email=None,
                to_emails=[getattr(user, "email", "Unknown")],
            ),
            context={"user": user, "activate_url": activate_url},
            templates=Templates(
                text_template="users/verify_account/confirm_message.txt",
                html_template="users/verify_account/confirm_message.html",
            ),
        )

        # Send account verification email
        email.send(fallback=False)

        # Return success response object
        return success_response(
            message="Sign up successful",
            data={"detail": "Success! Please check your email to verify your account."},
        )
