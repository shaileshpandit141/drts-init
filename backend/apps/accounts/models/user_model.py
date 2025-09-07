from __future__ import annotations

from typing import Any, ClassVar

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import (
    BigAutoField,
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    ImageField,
)
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.managers.user_manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email as the username field.

    instead of a username. Extends Django's AbstractBaseUser
    and PermissionsMixin.
    """

    class Meta(AbstractBaseUser.Meta, PermissionsMixin.Meta):  # type: ignore  # noqa: PGH003
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering: ClassVar[list[str]] = ["-last_login"]

    objects = UserManager()

    USERNAME_FIELD = "email"  # Use email as the unique identifier
    REQUIRED_FIELDS: ClassVar[
        list[str]
    ] = []  # Email & password are required by default

    id: BigAutoField[int, int] = BigAutoField(
        primary_key=True,
        unique=True,
        null=False,
        db_index=True,
        error_messages={"invalid": "Please enter a valid ID"},
    )

    email: EmailField[str, str] = EmailField(
        max_length=254,
        unique=True,
        null=False,
        blank=False,
        db_index=True,
        error_messages={
            "invalid": "Please enter a valid email address",
            "null": "Email address is required",
            "blank": "Email address cannot be empty",
        },
    )
    first_name: CharField[str | None, str | None] = CharField(
        max_length=30,
        unique=False,
        null=True,
        blank=True,
        db_index=False,
        default="",
        error_messages={
            "invalid": "Please enter a valid first name",
            "max_length": "First name cannot be longer than 30 characters",
        },
    )
    last_name: CharField[str | None, str | None] = CharField(
        max_length=30,
        unique=False,
        null=True,
        blank=True,
        db_index=False,
        default="",
        error_messages={
            "invalid": "Please enter a valid last name",
            "max_length": "Last name cannot be longer than 30 characters",
        },
    )
    picture = ImageField(
        upload_to="users/pictures/",
        max_length=100,
        null=True,
        blank=True,
        storage=None,
        db_index=False,
        default=None,
        error_messages={
            "invalid": "Please provide a valid image file",
            "invalid_image": "The uploaded file must be a valid image format like JPG, PNG or GIF",
            "missing": "Please select an image file to upload",
            "empty": "The uploaded file is empty. Please select a valid image file",
            "max_length": "The filename is too long. 100 characters allowed",
        },
    )
    is_active = BooleanField(
        default=True,
        null=False,
        db_index=False,
        error_messages={"invalid": "Please specify whether the user is active"},
    )
    is_verified: BooleanField[bool, bool] = BooleanField(
        default=False,
        null=False,
        db_index=False,
        error_messages={"invalid": "Please specify whether the account is verified"},
    )
    is_staff: BooleanField[bool, bool] = models.BooleanField(
        default=False,
        null=False,
        db_index=False,
        error_messages={"invalid": "Please specify whether the user is staff"},
    )
    is_superuser: BooleanField[bool, bool] = BooleanField(
        default=False,
        null=False,
        db_index=False,
        error_messages={"invalid": "Please specify whether the user is a superuser"},
    )
    date_joined: DateTimeField[str, str] = DateTimeField(
        auto_now=False,
        auto_now_add=True,
        null=False,
        blank=False,
        db_index=False,
        error_messages={"invalid": "Please enter a valid date and time"},
    )
    last_login: DateTimeField[str, str] = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=False,
        blank=False,
        db_index=False,
        error_messages={"invalid": "Please enter a valid date and time"},
    )

    def __str__(self) -> str:
        """Returns the string representation of the user (email)."""
        return str(self.email)

    def get_full_name(self) -> str:
        """Return full name otherwise email fallback"""
        if self.first_name or self.last_name:
            return f"{self.first_name or ''} {self.last_name or ''}".strip()
        return self.email  # fallback

    def get_short_name(self) -> str:
        """Return short name base on it's presence."""
        return self.first_name or self.email

    def update_login_timestamp(self) -> None:
        """Update last_login timestamp"""
        self.last_login = str(timezone.now())
        self.save(update_fields=["last_login"])

    def get_jwt_tokens(self) -> dict[str, Any]:
        """Generate Jwt tokens."""
        refresh_token = RefreshToken.for_user(self)
        tokens: dict[str, Any] = {
            "refresh_token": str(refresh_token),
            "access_token": str(refresh_token.access_token),
        }
        # Update last_login timestamp
        self.update_login_timestamp()
        return tokens
