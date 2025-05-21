from rest_core.serializers.mixins import FileFieldUrlMixin
from rest_framework.serializers import ModelSerializer
from user_auth.models import User


class UserPublicSerializer(FileFieldUrlMixin, ModelSerializer):
    """Serializer for User model that handles serialization and
    deserialization of User objects.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "picture",
            "is_verified",
            "is_staff",
            "is_superuser",
        ]
        read_only_fields = [
            "id",
            "email",
            "username",
            "is_verified",
            "is_staff",
            "is_superuser",
        ]
