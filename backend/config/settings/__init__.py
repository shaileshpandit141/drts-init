from envconfig import config

environ = config.ENVIRONMENT

# Import settings based on environment
if environ == "dev":
    from .environments.development import *
elif environ == "prod":
    from .environments.production import *
else:
    msg: str = "Please define the Environ mode as dev, prod"
    raise EnvironmentError(msg)
