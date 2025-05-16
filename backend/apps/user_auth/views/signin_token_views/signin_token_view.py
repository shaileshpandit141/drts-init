from apps.user_auth.throttles import AuthUserRateThrottle
from core.get_jwt_tokens_for_user import get_jwt_tokens_for_user
from django.utils import timezone
from rest_core.response import failure_response, success_response
from rest_core.views.mixins import ModelObjectMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from user_auth.models import User


class SigninTokenView(ModelObjectMixin[User], APIView):
    """API view for signing in users and generating JWT tokens."""

    throttle_classes = [AuthUserRateThrottle]
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs) -> Response:
        # Get required data from request
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        # Handle if user not include email in payload
        if email is None:
            return failure_response(
                message="Sign in failed - Email required",
                errors={"email": ["Please enter your email address"]},
            )

        # Handle if user not include password in payload
        if password is None:
            return failure_response(
                message="Sign in failed - Password required",
                errors={"password": ["Please enter your password"]},
            )

        # Handle email and username based signin
        try:
            user = None
            if "@" in email:
                user = self.get_object(email=email)
            else:
                user = self.get_object(username=email)

            # Check is user is None
            if user is None:
                return failure_response(
                    message="Sign in failed - Invalid credentials",
                    errors={
                        "password": [
                            "Invalid credentials. Please check your email/username and try again."
                        ]
                    },
                )

            # Check user password is currect or not
            if not user.check_password(password):
                return failure_response(
                    message="Sign in failed - Invalid password",
                    errors={"password": ["Invalid password. Please try again."]},
                )

            # Handle success signin response
            if not user.is_superuser and not user.is_verified:
                return failure_response(
                    message="Sign in failed - Email verification required",
                    errors={"detail": "Please verify your account to sign in."},
                )

            # Generate jwt toke for requested user
            jwt_tokens = get_jwt_tokens_for_user(user)

            # Update last login timestamp
            if user:
                setattr(user, "last_login", timezone.now())
                user.save(update_fields=["last_login"])

            # Return success response
            return success_response(
                message="Welcome back! You have successfully signed in", data=jwt_tokens
            )
        except Exception:
            return failure_response(
                message="Sign in failed",
                errors={"detail": "Somethings is wrong!. Please try again."},
            )
