from typing import Any

from django.contrib.auth.models import BaseUserManager


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
