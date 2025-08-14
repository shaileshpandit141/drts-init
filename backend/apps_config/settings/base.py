from datetime import timedelta
from pathlib import Path
from typing import Any

from core.environment import GetEnv

# Configuration Settings File for the django backend
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security Configuration Settings
# -------------------------------
SECRET_KEY: str = GetEnv.str("SECRET_KEY")

# DEBUG Configuration Settings
# ----------------------------
DEBUG = False

# Allowed Host Configuration Settings
# -----------------------------------
ALLOWED_HOSTS: list[str] = GetEnv.list("HOST")

# Frontend URL Configuration Setting
# ----------------------------------
FRONTEND_URL = GetEnv.str("FRONTEND_URL")

# Configure CORS Settings
# -----------------------
CORS_ALLOWED_ORIGINS: list[str] = GetEnv.list("CORS_ALLOWED_ORIGINS")

# Login Redirect URL Configuration Setting
# ----------------------------------------
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL

# Django built-in applications settings
# -------------------------------------
INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# Third-party applications Settings
# ---------------------------------
INSTALLED_APPS.extend(
    [
        "rest_framework",
        "rest_framework_simplejwt",
        "rest_framework_simplejwt.token_blacklist",
        "corsheaders",
        "rest_core",
    ]
)

# User Define applications Settings
# ---------------------------------
INSTALLED_APPS.extend(
    [
        "apps.accounts.apps.AccountsConfig",
        "apps.google_auth.apps.GoogleAuthConfig",
    ]
)

# Middleware Configuration Settings
# ---------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "rest_core.middlewares.ResponseTimeMiddleware",
]

# Root urls file Configuration Settings
# -------------------------------------
ROOT_URLCONF = "apps_config.urls"

# Templates Configuration Settings
# --------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Application Server Configuration Setting
# ----------------------------------------
ASGI_APPLICATION = "apps_config.asgi.application"

# User Model Configuration Setting
# --------------------------------
AUTH_USER_MODEL = "accounts.User"

# Default primary key field type Configuration Setting
# ----------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password Validators Configuration Settings
# ------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Password hashing algorithms in order of preference
# Using multiple algorithms provides additional security layers
# -------------------------------------------------------------
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
]

# Internationalization Configuration Settings
# -------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# STATIC AND MEDIA FILES Configuration Settings
# ---------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Configure media files (User-uploaded files)
# -------------------------------------------
MEDIA_ROOT = BASE_DIR / "uploads"
MEDIA_URL = "/media/"

# REST Framework Configuration Settings
# -------------------------------------
REST_FRAMEWORK = {
    "NON_FIELD_ERRORS_KEY": "non_field",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "EXCEPTION_HANDLER": "rest_core.exceptions.base_exception_handler",
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_core.renderers.StructuredJSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/day",
        "auth": "8/hour",
        "user": "1000/day",
    },
    "DEFAULT_PAGINATION_CLASS": "rest_core.pagination.PageNumberPagination",
    "PAGE_SIZE": 4,
    "MAX_PAGE_SIZE": 8,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}

# JWT Token Configuration Settings
# --------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=20),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(minutes=20),
}

# Authentication Configuration Settings
# -------------------------------------
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

# EMAIL Configuration Settings
# ----------------------------
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = GetEnv.str("EMAIL_BACKEND")  # type: ignore[]
    EMAIL_HOST = GetEnv.str("EMAIL_HOST")
    EMAIL_PORT = GetEnv.int("EMAIL_PORT")
    EMAIL_USE_TLS = GetEnv.bool("EMAIL_USE_TLS", default=True)
    EMAIL_USE_SSL = GetEnv.bool("EMAIL_USE_SSL", default=False)
    EMAIL_HOST_USER = GetEnv.str("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = GetEnv.str("EMAIL_HOST_PASSWORD")
    DEFAULT_FROM_EMAIL = GetEnv.str(
        "DEFAULT_FROM_EMAIL",
        default=EMAIL_HOST_USER,
    )

# Google OAuth2 Configuration Settings
# ------------------------------------
GOOGLE_CLIENT_ID = GetEnv.str("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = GetEnv.str("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = GetEnv.str("GOOGLE_REDIRECT_URI")

# Redis configuration for production
# ----------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": GetEnv.str("REDIS_CACHE_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Celery Configuration Settings
# -----------------------------
# Redis as broker
CELERY_BROKER_URL = "redis://localhost:6379/0"

# Where results are stored
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

# Recommended settings
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# Task time limits (avoid runaway tasks)
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 mins
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60

# Log-Related Directory Configuration Setup
# -----------------------------------------
LOG_DIR = BASE_DIR / "logs"

# Create log directory if it doesn't exist
# ----------------------------------------
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Logging Configuration Settings
# ------------------------------
LOGGING: dict[str, Any] = {
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
            "filename": LOG_DIR / "django.log",
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
