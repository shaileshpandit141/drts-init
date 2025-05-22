from typing import Any

from django.utils import timezone
from rest_framework.serializers import CharField, Serializer, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from user_auth.models import User


class SigninSerializer(Serializer):
    """Serializer for user sign-in."""

    email = CharField(write_only=True, style={"input_type": "text"})
    password = CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validate the input data for user sign-in."""

        # Extract signin credentials from the request
        email = attrs.get("email", "").strip()
        password = attrs.get("password")

        # Handle email and username based signin
        user = None
        if "@" in email:
            user = User.objects.filter(email__iexact=email).first()
        else:
            user = User.objects.filter(username__iexact=email).first()

        # Checking if user is None
        if user is None:
            raise ValidationError(
                {"email": ["Invalid email or username. Please try again."]},
                code="invalid_credentials",
            )

        # Checking if the user is active or not
        if not user.is_active:
            raise ValidationError(
                "User account is inactive. Please contact support.",
                code="inactive_account",
            )

        # Checking if the password is empty or not
        if not password:
            raise ValidationError(
                {"password": ["Password is required. Please try again."]},
                code="password_required",
            )

        # Check if the password is correct or not
        if not user.check_password(password):
            raise ValidationError(
                {"password": ["Invalid password. Please try again."]},
                code="invalid_password",
            )

        # Check whether the user is verified or not
        if not user.is_superuser and not getattr(user, "is_verified", True):
            raise ValidationError(
                "Please verify your account to sign in.",
                code="account_not_verified",
            )

        # Attech user to use later in create or get_jwt_tokens
        attrs["user"] = user
        return attrs

    def create(self, validated_data: dict[str, Any]) -> dict[str, str]:
        """Generate JWT tokens for the authenticated user."""
        user = validated_data["user"]
        return self.get_jwt_tokens(user)

    def get_jwt_tokens(self, user: User) -> dict[str, str]:
        """Generate JWT tokens using Simple JWT."""
        refresh = RefreshToken.for_user(user)

        # Getting the access token from refresh token
        access_token = getattr(refresh, "access_token", None)

        # Checking if access token is None or not
        if access_token is None:
            raise ValidationError(
                "Failed to generate refresh token.",
                code="token_generation_failed",
            )

        # Update last login timestamp
        if user:
            setattr(user, "last_login", timezone.now())
            user.save(update_fields=["last_login"])

        # Finaly returning the tokens
        return {
            "refresh_token": str(refresh),
            "access_token": str(access_token),
        }
