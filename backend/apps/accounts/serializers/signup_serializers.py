from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from univalidator.composites import CompositeValidator
from univalidator.validators import MXEmailRecordValidator, RegexEmailValidator

from apps.accounts.models import User


class SignupSerializer(serializers.Serializer[User]):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="This email address is already taken.",
            )
        ]
    )
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    confirm_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        """Validate the input data for user signup."""
        email = attrs.get("email", "")
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        # Validate the email address
        email_validator = CompositeValidator[str](
            validators=[
                RegexEmailValidator(),
                MXEmailRecordValidator(),
            ]
        )

        if not email_validator.validate(email):
            raise serializers.ValidationError(
                detail=email_validator.errors,
                code="invalid_email",
            )

        if password is None:
            raise serializers.ValidationError(
                detail=["Password field can't be null"],
                code="invalid_password",
            )

        # Validate password meets requirements
        try:
            validate_password(password)
        except ValidationError as error:
            raise serializers.ValidationError({"password": error.messages}) from error

        # Validate password and confirm password match or not
        if password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Password and confirm password do not match."}
            )

        # Return the validated data
        return attrs

    def create(self, validated_data: dict[str, str]) -> User:
        email = validated_data["email"]
        password = validated_data.pop("password")

        # Create a new user instance
        user = User(email=email)

        # Set the password for the user
        user.set_password(password)
        user.save()

        # Return the created user instance
        return user
