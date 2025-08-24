from typing import Literal

from djresttoolkit.envconfig import EnvBaseSettings
from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    engine: str
    name: str
    user: str
    password: str
    host: str
    port: int


class RedisConfig(BaseModel):
    cache_location: str


class EmailConfig(BaseModel):
    backend: str
    host: str
    port: int
    use_tls: bool
    use_ssl: bool
    host_user: str
    host_password: str
    default_from_email: str


class GoogleOAuth2Config(BaseModel):
    client_id: str
    client_secret: str
    redirect_url: str


class CeleryConfig(BaseModel):
    broker_url: str
    result_backend: str


class EnvSettings(EnvBaseSettings["EnvSettings"]):
    """Env Settings class to handle env loads."""

    secret_key: str
    host: str
    port: int
    environ: Literal["dev", "prod"]
    allowed_hosts: list[str]
    cors_allowed_origins: list[str]
    database: DatabaseConfig
    redis: RedisConfig
    email: EmailConfig
    google: GoogleOAuth2Config
    celery: CeleryConfig


env_settings = EnvSettings.load(warning=False)
