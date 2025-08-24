"""
Django's command-line utility for administrative tasks.

This script serves as the main entry point for Django management commands.
It handles configuration of the Django environment and executes administrative tasks.
"""

import os
import sys

from envconfig import env_settings


def main() -> None:
    """
    Main function that runs Django administrative tasks.

    This function:
    1. Sets up the Django settings module
    2. Configures host and port from environment variables
    3. Executes Django management commands

    The host and port can be configured via environment variables:
    - HOST: The host to run the server on (default: localhost)
    - PORT: The port number to use (default: 8000)
    """
    # Set the Django settings module path
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appsconfig.settings")

    try:
        from django.core.management import execute_from_command_line  # noqa: PLC0415
    except ImportError as exc:
        msg: tuple[str, str, str] = (
            "Could not import Django. Are you sure it is installed and",
            "available on your PYTHONPATH environment variable? Did you",
            "forget to activate a virtual environment?",
        )
        raise ImportError(*msg) from exc

    # If no command is provided or the command is 'runserver',
    # append the host:port configuration to the command
    if len(sys.argv) == 1 or sys.argv[1] == "runserver":
        sys.argv = [*sys.argv[:2], f"{env_settings.host}:{env_settings.port}"]

    # Execute the Django management command
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
