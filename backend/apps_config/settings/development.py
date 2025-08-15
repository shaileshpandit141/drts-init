# Import all Settings from base configuration
# -------------------------------------------
from datetime import timedelta

from .base import *  # noqa: F403
from .base import BASE_DIR, LOGGING, REST_FRAMEWORK, SIMPLE_JWT

# Enable debug mode for development purposes only
# -----------------------------------------------
DEBUG = True  # type: ignore[]

# Configure Logging for development
# ---------------------------------
LOGGING["loggers"]["django"]["level"] = "DEBUG"

# REST Framework Configuration Settings
# -------------------------------------
REST_FRAMEWORK.update(
    {
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework_simplejwt.authentication.JWTAuthentication",
            "rest_framework.authentication.SessionAuthentication",
        ],
        "DEFAULT_RENDERER_CLASSES": [
            "rest_core.renderers.StructuredJSONRenderer",
            "rest_framework.renderers.BrowsableAPIRenderer",
        ],
        "PAGE_SIZE": 4,
        "MAX_PAGE_SIZE": 8,
    }
)

# JWT Token Configuration Settings
# --------------------------------
SIMPLE_JWT.update(
    {
        "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
        "REFRESH_TOKEN_LIFETIME": timedelta(minutes=20),
        "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
        "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(minutes=20),
    }
)

# SQLite Database Configuration for development environment
# ---------------------------------------------------------
DATABASES: dict[str, dict[str, object]] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
