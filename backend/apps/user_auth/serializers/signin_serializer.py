from typing import Any

from rest_framework.serializers import Serializer, CharField, ValidationError
from user_auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class SigninSerializer(Serializer):
    """Serializer for user sign-in."""

    email = CharField(write_only=True, style={"input_type": "text"})
    password = CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs) -> Any:
        """Validate the input data for user sign-in."""

        # Extract signin credentials from the request
        email = attrs.get("email", "")
        password = attrs.get("password")

        # Handle email and username based signin
        if "@" in email:
            user = User.objects.filter(email=email).first()
        else:
            user = User.objects.filter(username=email).first()

        # Check if user is None
        if user is None:
            raise ValidationError(
                detail="Invalid credentials. Please check your email/username and try again.",
                code="invalid_credentials",
            )

        # Check if the user is active or not
        if not user.is_active:
            raise ValidationError(
                detail="User account is inactive.",
                code="inactive_account",
            )

        # Check if the password is correct or not
        if not user.check_password(password):
            raise ValidationError(
                detail="Invalid password. Please try again with the correct password.",
                code="invalid_password",
            )

        # Check whether the user is verified or not
        if not user.is_superuser and not user.is_verified:
            raise ValidationError(
                detail="Please verify your account to sign in.",
                code="account_not_verified",
            )

        # Attech user to use later in create or get_jwt_tokens
        attrs["user"] = user

        # Return the validated data
        return attrs

    def create(self, validated_data) -> Any:
        """Create a user instance and generate JWT tokens."""
        # Extract user from validated data
        user = validated_data.get("user")

        # Generate JWT tokens for the user
        jwt_tokens = self.get_jwt_tokens(user)

        # Return the JWT tokens
        return jwt_tokens

    def get_jwt_tokens(self, user) -> dict[str, str]:
        """Generate JWT tokens for the user."""

        refresh = RefreshToken.for_user(user)
        return {
            "refresh_token": str(refresh),
            "access_token": str(getattr(refresh, "access_token", "")),
        }
