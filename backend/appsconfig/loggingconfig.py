from pathlib import Path
from typing import Any


def get_logging(log_dir: Path) -> dict[str, Any]:
    """Return logging config settings."""
    log_dir.mkdir(parents=True, exist_ok=True)

    return {
        "version": 1,  # Version of the logging configuration
        "disable_existing_loggers": False,  # Keep default loggers like Django"s
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
                "style": "{",
            },
            "simple": {
                "format": "\033[1;36m{levelname}\033[0m {message}\n",
                "style": "{",
            },
            "colorful": {
                "()": "colorlog.ColoredFormatter",
                "format": "%(log_color)s%(levelname)-8s%(reset)s %(message)s\n",
                "log_colors": {
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                },
            },
        },
        "filters": {
            "require_debug_false": {
                "()": "django.utils.log.RequireDebugFalse",
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "colorful",
            },
            "file": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": log_dir / "django.log",
                "maxBytes": 5 * 1024 * 1024,  # 5MB per file
                "backupCount": 3,  # Keep last 3 log files
                "formatter": "verbose",
            },
            "mail_admins": {
                "level": "ERROR",
                "class": "django.utils.log.AdminEmailHandler",
                "filters": ["require_debug_false"],
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": True,
            },
            "django.request": {
                "handlers": ["mail_admins", "file"],
                "level": "ERROR",
                "propagate": False,
            },
            "custom_logger": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
            },
        },
    }
