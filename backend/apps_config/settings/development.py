# Import all Settings from base configuration
# -------------------------------------------
from datetime import timedelta

from decouple import Csv, config

from .base import *
from .base import BASE_DIR, LOGGING, REST_FRAMEWORK, SIMPLE_JWT

# Enable debug mode for development purposes only
# -----------------------------------------------
DEBUG = True

# Configure Logging for development
# ---------------------------------
LOGGING["loggers"]["django"]["level"] = "DEBUG"

# List of host/domain names that Django can serve
# -----------------------------------------------
ALLOWED_HOSTS = config("HOST", cast=Csv())

# Configure CORS Settings
# -----------------------
CORS_ALLOWED_ORIGINS = config("FRONTEND_URL", cast=Csv())

# REST Framework Configuration Settings
# -------------------------------------
REST_FRAMEWORK.update(
    {
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
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Memcached configuration for testing environment
# -----------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}
