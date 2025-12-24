from .apps import *
from .middlewares import *
from .cache import *
from .celery import *
from pathlib import Path
from typing import Any
from envconfig import config
from config.logging import get_logging

# Configuration Settings File for the django backend
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

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

# Root urls file Configuration Settings
# -------------------------------------
ROOT_URLCONF = "config.urls"

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
ASGI_APPLICATION = "config.asgi.application"

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

# Logging Configuration Settings
# ------------------------------
LOGGING: dict[str, Any] = get_logging(BASE_DIR / "logs")
