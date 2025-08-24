from typing import Any

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.serializers import CharField, Serializer, ValidationError

from apps.accounts.models import User


class PasswordChangeSerializer(Serializer[User]):
    """Serializer for changing user password."""

    current_password = CharField(write_only=True, style={"input_type": "password"})
    new_password = CharField(write_only=True, style={"input_type": "password"})
    confirm_password = CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validate the input data for user password change."""
        user: User = self.context["request"].user

        # Extract password change credentials from the request
        current_password = attrs.get("current_password", "")
        new_password = attrs.get("new_password", "")
        confirm_password = attrs.get("confirm_password")

        if not user.check_password(current_password):
            raise ValidationError(
                {"current_password": "Current password is incorrect."},
                code="invalid_password",
            )

        if new_password != confirm_password:
            raise ValidationError(
                {
                    "confirm_password": [
                        "New password and confirm password do not match."
                    ]
                },
                code="password_mismatch",
            )

        # Validate password meets requirements
        try:
            validate_password(new_password, user=user)
        except DjangoValidationError as error:
            raise ValidationError({"new_password": error.messages}) from error

        # Validate password and confirm password match or not
        if new_password != confirm_password:
            raise ValidationError(
                {"confirm_password": ["Password and confirm password do not match."]},
                code="password_mismatch",
            )

        # Check if the new password is the same as the current password
        if new_password == current_password:
            raise ValidationError(
                {
                    "confirm_password": [
                        "New password cannot be the same as the current password."
                    ]
                },
                code="same_password",
            )

        # Return the validated data
        return attrs

    def save(self, **kwargs: object) -> User:  # noqa: ARG002
        """Set the new password and return the updated user instance."""
        user = self.context["request"].user

        # Get new password from validated data
        new_password = self.validated_data["new_password"]

        # Set new password
        user.set_password(new_password)
        user.save(update_fields=["password"])

        # Return the updated user instance
        return user
