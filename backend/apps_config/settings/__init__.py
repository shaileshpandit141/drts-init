from env_config import env_settings

environ = env_settings.environ

# Import settings based on environment
if environ == "dev":
    from .development import *  # noqa: F403
elif environ == "prod":
    from .production import *  # noqa: F403
else:
    msg: str = "Please define the Environ mode as dev, prod"
    raise OSError(msg)
