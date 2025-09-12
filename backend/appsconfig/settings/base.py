from datetime import timedelta
from pathlib import Path
from typing import Any

from envconfig import config

from appsconfig.loggingconfig import get_logging

# Configuration Settings File for the django backend
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security Configuration Settings
# -------------------------------
SECRET_KEY = config.SECRET_KEY

# DEBUG Configuration Settings
# ----------------------------
DEBUG = False

# Allowed Host Configuration Settings
# -----------------------------------
ALLOWED_HOSTS = config.ALLOWED_HOSTS

# Configure CORS Settings
# -----------------------
CORS_ALLOWED_ORIGINS = config.CORS_ALLOWED_ORIGINS

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
        "djresttoolkit",
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
    "djresttoolkit.middlewares.ResponseTimeMiddleware",
]

# Root urls file Configuration Settings
# -------------------------------------
ROOT_URLCONF = "appsconfig.urls"

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
ASGI_APPLICATION = "appsconfig.asgi.application"

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
    "NON_FIELD_ERRORS_KEY": "non_field_errors",
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "EXCEPTION_HANDLER": "djresttoolkit.views.exception_handler",
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "djresttoolkit.renderers.ThrottleInfoJSONRenderer",
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
    "DEFAULT_PAGINATION_CLASS": "djresttoolkit.pagination.PageNumberPagination",
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
EMAIL_BACKEND = config.EMAIL_BACKEND
EMAIL_HOST = config.EMAIL_HOST
EMAIL_PORT = config.EMAIL_PORT
EMAIL_USE_TLS = config.EMAIL_USE_TLS
EMAIL_USE_SSL = config.EMAIL_USE_SSL
EMAIL_HOST_USER = config.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = config.EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = config.EMAIL_DEFAULT_FROM_EMAIL


# Google OAuth2 Configuration Settings
# ------------------------------------
GOOGLE_CLIENT_ID = config.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = config.GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_URI = config.GOOGLE_REDIRECT_URI

# Redis configuration for production
# ----------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config.REDIS_CACHE_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Celery Configuration Settings
# -----------------------------
# Redis as broker
CELERY_BROKER_URL = config.CELERY_BROKER_URL

# Where results are stored
CELERY_RESULT_BACKEND = config.CELERY_RESULT_BACKEND

# Recommended settings
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# Task time limits (avoid runaway tasks)
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 mins
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60

# Logging Configuration Settings
# ------------------------------
LOGGING: dict[str, Any] = get_logging(BASE_DIR / "logs")
