"""Django's command-line utility for administrative tasks."""

import os
import sys


def main() -> None:
    """Main function that runs Django administrative tasks."""

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

    # Execute the Django management command
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
