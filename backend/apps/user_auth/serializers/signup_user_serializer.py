from typing import Any
from rest_framework import serializers
from user_auth.models import User


class SignupUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    confirm_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    def validate(self, attrs) -> Any:
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Password and confirm password do not match."}
            )

        return attrs

    def create(self, validated_data: dict) -> User:
        email = validated_data.get("email", "")
        username = email.split("@")[0]
        password = validated_data.pop("password")

        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return user
