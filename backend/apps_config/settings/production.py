# Import all Settings from base configuration
# -------------------------------------------
from datetime import timedelta

from core.environment import GetEnv

from .base import *  # noqa: F403
from .base import LOGGING, REST_FRAMEWORK

# Disable debug mode for production environment for security
# ----------------------------------------------------------
DEBUG = False  # type: ignore[]

# Configure Logging for production
# --------------------------------
LOGGING["loggers"]["django"]["level"] = "INFO"

# REST Framework Configuration Settings
# -------------------------------------
REST_FRAMEWORK.update(
    {
        "DEFAULT_RENDERER_CLASSES": [
            "rest_core.renderers.StructuredJSONRenderer",
        ],
        "PAGE_SIZE": 16,
        "MAX_PAGE_SIZE": 32,
    }
)

# JWT Token Configuration Settings
# --------------------------------
SIMPLE_JWT.update(  # noqa: F405
    {
        "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
        "REFRESH_TOKEN_LIFETIME": timedelta(minutes=1),
        "SLIDING_TOKEN_LIFETIME": timedelta(minutes=60),
        "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(minutes=1),
    }
)

# PostgreSQL database configuration Settings
# ------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": GetEnv.str("DB_NAME"),
        "USER": GetEnv.str("DB_USER"),
        "PASSWORD": GetEnv.str("DB_PASSWORD"),
        "HOST": GetEnv.str("DB_HOST"),
        "PORT": GetEnv.str("DB_PORT"),
    }
}


# Security Settings for production environment
# These settings ensure secure communication and protect against common vulnerabilities
# -------------------------------------------------------------------------------------
CSRF_COOKIE_SECURE = True  # Enforce HTTPS for CSRF cookies
SESSION_COOKIE_SECURE = True  # Enforce HTTPS for session cookies
SECURE_BROWSER_XSS_FILTER = True  # Activate browser's XSS filtering
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME-type sniffing security risks
SECURE_SSL_REDIRECT = True  # Force all connections to use HTTPS
