from typing import Any
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
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

        # Validate password meets requirements
        try:
            validate_password(password)
        except ValidationError:
            raise serializers.ValidationError(
                {"password": ["Password does not meet the requirements."]}
            )

        # Validate password and confirm password match or not
        if password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Password and confirm password do not match."}
            )

        # Return the validated data
        return attrs

    def create(self, validated_data: dict) -> User:
        email = validated_data.get("email", "")
        username = email.split("@")[0]
        password = validated_data.pop("password")

        # Create a new user instance
        user = User(
            username=username,
            email=email,
        )

        # Set the password for the user
        user.set_password(password)
        user.save()

        # Return the created user instance
        return user
