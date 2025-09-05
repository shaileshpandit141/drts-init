from typing import Literal
from djresttoolkit.envconfig import BaseEnvConfig


class EnvConfig(BaseEnvConfig):
    # Server running environment.
    ENVIRONMENT: Literal["dev", "prod"] = "prod"

    # Core Django related config.
    SECRET_KEY: str
    ALLOWED_HOSTS: list[str] = [
        "localhost",
        "127.0.0.1",
    ]

    # Cors origins related config.
    CORS_ALLOWED_ORIGINS: list[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # DB related config.
    DB_ENGINE: str = "django.db.backends.postgresql"
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int

    # Email related config.
    EMAIL_BACKEND: str
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USE_TLS: bool = True
    EMAIL_USE_SSL: bool = False
    EMAIL_HOST_USER: str
    EMAIL_HOST_PASSWORD: str
    EMAIL_DEFAULT_FROM_EMAIL: str

    # Google oauth2 related config.
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # Redis related config.
    REDIS_CACHE_LOCATION: str = "redis://127.0.0.1:6379/1"

    # Celery related config.
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str


# Creating env config instance.
config = EnvConfig()
