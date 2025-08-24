from typing import Any

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):  # type: ignore  # noqa: PGH003
    """
    Custom user manager that extends Django's BaseUserManager.

    To handle email-based authentication. Provides methods for
    creating regular users and superusers.
    """

    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,  # noqa: ANN401
    ) -> Any:  # noqa: ANN401
        """Creates and saves a User with the given email and password."""
        if not email:
            msg = "The Email field must be set"
            raise ValueError(msg)

        # Normalize and validate email
        email = self.normalize_email(email)
        if "@" not in email:
            msg = "Invalid email address"
            raise ValueError(msg)

        # Create and save user
        user = self.model(email=email, **extra_fields)  # type: ignore  # noqa: PGH003
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,  # noqa: ANN401
    ) -> Any:  # noqa: ANN401
        """
        Creates and saves a superuser with the given email and password.

        Sets is_staff, is_superuser and is_active to True by default.
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            msg = "Superuser must have is_staff=True."
            raise ValueError(msg)
        if extra_fields.get("is_superuser") is not True:
            msg = "Superuser must have is_superuser=True."
            raise ValueError(msg)

        return self.create_user(email, password, **extra_fields)
