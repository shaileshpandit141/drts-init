from typing import Any

from rest_framework.serializers import (
    CharField,
    EmailField,
    Serializer,
    ValidationError,
)

from apps.accounts.models import User


class RetriveTokenSerializer(Serializer[User]):
    email = EmailField(style={"input_type": "text"})
    password = CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validate the input data for user sign-in."""
        email = attrs["email"].strip()
        password: str = attrs["password"]

        # Handle email based signin
        user = User.objects.filter(email__iexact=email).first()

        # Checking if user is None
        if user is None:
            raise ValidationError(
                {"email": ["Invalid email address. Please try again."]},
                code="invalid_credentials",
            )

        # Checking if the user is active or not
        if not user.is_active:
            msg: str = "User account is inactive. Please contact support."
            raise ValidationError(msg, code="inactive_account")

        # Check if the password is correct or not
        if not user.check_password(password):
            raise ValidationError(
                {"password": ["Invalid password. Please try again."]},
                code="invalid_password",
            )

        # Check whether the user is verified or not
        if not user.is_superuser and not user.is_verified:
            msgx: str = "Please verify your account to sign in."
            raise ValidationError(msgx, code="account_not_verified")

        # Attech user to use later in create or get_jwt_tokens
        attrs["user"] = user
        return attrs

    def create(self, validated_data: dict[str, Any]) -> User:
        """Generate JWT tokens for the authenticated user."""
        user = validated_data["user"]
        return user
