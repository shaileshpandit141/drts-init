from typing import Any

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager that extends Django's BaseUserManager
    to handle email-based authentication. Provides methods for
    creating regular users and superusers.
    """

    def create_user(self, email, password=None, **extra_fields) -> Any:
        """Creates and saves a User with the given email and password."""

        if not email:
            raise ValueError("The Email field must be set")

        # Normalize and validate email
        email = self.normalize_email(email)
        if "@" not in email:
            raise ValueError("Invalid email address")

        # Set username from email
        extra_fields["username"] = email.split("@")[0]

        # Create and save user
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields) -> Any:
        """Creates and saves a superuser with the given email and password.
        Sets is_staff, is_superuser and is_active to True by default.
        """

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that uses email as the username field
    instead of a username. Extends Django's AbstractBaseUser
    and PermissionsMixin.
    """

    class Meta(AbstractBaseUser.Meta, PermissionsMixin.Meta):  # type: ignore
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-last_login"]

    objects = UserManager()

    USERNAME_FIELD = "email"  # Use email as the unique identifier
    REQUIRED_FIELDS = []  # Email & password are required by default

    email = models.EmailField(
        max_length=254,
        unique=True,
        null=False,
        blank=False,
        db_index=True,
        default="",
        error_messages={
            "invalid": "Please enter a valid email address",
            "null": "Email address is required",
            "blank": "Email address cannot be empty",
        },
    )
    username = models.CharField(
        max_length=30,
        unique=True,
        null=False,
        blank=False,
        db_index=False,
        default="",
        error_messages={
            "invalid": "Please enter a valid last name",
            "null": "Last name is required",
            "blank": "Last name cannot be empty",
            "max_length": "Last name cannot be longer than 30 characters",
        },
    )
    first_name = models.CharField(
        max_length=30,
        unique=False,
        null=True,
        blank=True,
        db_index=False,
        default="",
        error_messages={
            "invalid": "Please enter a valid first name",
            "null": "First name is required",
            "blank": "First name cannot be empty",
            "max_length": "First name cannot be longer than 30 characters",
        },
    )
    last_name = models.CharField(
        max_length=30,
        unique=False,
        null=True,
        blank=True,
        db_index=False,
        default="",
        error_messages={
            "invalid": "Please enter a valid last name",
            "null": "Last name is required",
            "blank": "Last name cannot be empty",
            "max_length": "Last name cannot be longer than 30 characters",
        },
    )
    picture = models.ImageField(
        upload_to="users/pictures/",
        max_length=100,
        null=False,
        blank=False,
        storage=None,
        db_index=False,
        default="users/pictures/default.png",
        error_messages={
            "invalid": "Please provide a valid image file",
            "invalid_image": "The uploaded file must be a valid image format like JPG, PNG or GIF",
            "missing": "Please select an image file to upload",
            "empty": "The uploaded file is empty. Please select a valid image file",
            "max_length": "The filename is too long. 100 characters allowed",
            "null": "An picture image is required",
            "blank": "An picture image is required",
        },
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        db_index=False,
        error_messages={
            "invalid": "Please specify whether the user is active",
            "null": "Active status is required",
            "blank": "Active status cannot be empty",
        },
    )
    is_staff = models.BooleanField(
        default=False,
        null=False,
        db_index=False,
        error_messages={
            "invalid": "Please specify whether the user is staff",
            "null": "Staff status is required",
            "blank": "Staff status cannot be empty",
        },
    )
    is_superuser = models.BooleanField(
        default=False,
        null=False,
        db_index=False,
        error_messages={
            "invalid": "Please specify whether the user is a superuser",
            "null": "Superuser status is required",
            "blank": "Superuser status cannot be empty",
        },
    )
    is_verified = models.BooleanField(
        default=False,
        null=False,
        db_index=False,
        error_messages={
            "invalid": "Please specify whether the account is verified",
            "null": "Account verification status is required",
            "blank": "Account verification status cannot be empty",
        },
    )
    date_joined = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        null=False,
        blank=False,
        db_index=False,
        error_messages={
            "invalid": "Please enter a valid date and time",
            "null": "Date joined is required",
            "blank": "Date joined cannot be empty",
        },
    )
    last_login = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=False,
        blank=False,
        db_index=False,
        error_messages={
            "invalid": "Please enter a valid date and time",
            "null": "Last login date is required",
            "blank": "Last login date cannot be empty",
        },
    )

    def __str__(self) -> str:
        """Returns the string representation of the user (email)"""
        return str(self.email)

    def get_short_name(self) -> str:
        """Returns the user's first name if it exists"""
        return (str(self.first_name)).strip()

    def get_full_name(self) -> str | None:
        """Returns the user"s full name, with a space between
        first and last name. If exist otherwise None
        """
        if self.first_name is None or self.last_name is None:
            return None
        return f"{self.first_name} {self.last_name}".strip()
