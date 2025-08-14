from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Django app configuration for the users app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    label = "accounts"
