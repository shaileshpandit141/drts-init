from rest_core.serializers.mixins import FileFieldUrlMixin
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from user_auth.models import User


class UserSerializer(FileFieldUrlMixin, ModelSerializer):
    """Serializer for User model that handles serialization and
    deserialization of User objects.
    """

    # Get the full name of the user
    full_name = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "picture",
            "is_verified",
            "is_staff",
            "is_superuser",
        ]
        read_only_fields = [
            "id",
            "email",
            "is_verified",
            "is_staff",
            "is_superuser",
        ]

    def get_full_name(self, obj) -> str:
        """Return the full name of the user."""
        return obj.get_full_name()
