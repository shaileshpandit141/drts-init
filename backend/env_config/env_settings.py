import warnings
from pathlib import Path
from typing import Any, ClassVar, Literal

import yaml  # type: ignore # noqa: PGH003
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


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


class EnvSettings(BaseSettings):
    """Env Settings class to handle env loads."""

    env_file: str = ".env"
    yaml_file: ClassVar[str] = ".environ.yaml"

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

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    @classmethod
    def load(
        cls,
        *,
        env_file: str | None = None,
        ymal_file: str | None = None,
        warning: bool = True,
    ) -> "EnvSettings":
        """Load from YAML first, then override with .env."""
        if env_file:
            cls.env_file = env_file
        if ymal_file:
            cls.yaml_file = ymal_file

        config_file = Path(cls.yaml_file)
        yaml_data: dict[str, Any] = {}
        if config_file.exists():
            with config_file.open("r") as f:
                yaml_data = yaml.safe_load(f) or {}
        elif warning:
            msg: str = f"Config file {config_file} not found, using only env vars."
            warnings.warn(msg, UserWarning, stacklevel=1)

        return cls(**yaml_data)


env_settings = EnvSettings.load(warning=False)
