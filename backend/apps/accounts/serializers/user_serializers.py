from typing import ClassVar

from rest_core.serializers.mixins import FileFieldUrlMixin
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from apps.accounts.models import User


class UserSerializer(FileFieldUrlMixin, ModelSerializer[User]):
    """Serializer for User model."""

    # Get the full name of the user
    full_name = SerializerMethodField(read_only=True)

    class Meta:  # type: ignore[override]
        model = User
        fields: ClassVar[list[str]] = [
            "id",
            "full_name",
            "email",
            "username",
            "first_name",
            "last_name",
            "picture",
            "is_staff",
            "is_superuser",
            "is_verified",
        ]
        read_only_fields: ClassVar[list[str]] = [
            "id",
            "email",
            "is_verified",
            "is_staff",
            "is_superuser",
        ]

    def get_full_name(self, obj: User) -> str:
        """Return the full name."""
        return obj.get_full_name()


class UserPublicSerializer(FileFieldUrlMixin, ModelSerializer[User]):
    """Serializer for User model."""

    # Get the full name of the user
    full_name = SerializerMethodField(read_only=True)

    class Meta:  # type: ignore[override]
        model = User
        fields: ClassVar[list[str]] = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "picture",
        ]
        read_only_fields: ClassVar[list[str]] = [
            "id",
            "email",
        ]

    def get_full_name(self, obj: User) -> str:
        """Return the full name of the user."""
        return obj.get_full_name()
