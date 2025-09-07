from typing import ClassVar

from djresttoolkit.serializers.mixins import AbsoluteUrlFileMixin
from rest_framework.serializers import ModelSerializer

from apps.accounts.models import User


class UserSerializer(AbsoluteUrlFileMixin, ModelSerializer[User]):
    """Serializer for User model."""

    class Meta:  # type: ignore[override]
        model = User
        fields: ClassVar[list[str]] = [
            "email",
            "first_name",
            "last_name",
            "picture",
            "is_verified",
            "is_staff",
            "is_superuser",
        ]
        read_only_fields: ClassVar[list[str]] = [
            "email",
            "is_verified",
            "is_staff",
            "is_superuser",
        ]
