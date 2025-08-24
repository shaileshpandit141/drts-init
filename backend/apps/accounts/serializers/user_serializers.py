from typing import ClassVar

from djresttoolkit.serializers.mixins import AbsoluteUrlFileMixin
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from apps.accounts.models import User


class UserSerializer(AbsoluteUrlFileMixin, ModelSerializer[User]):
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
