from decouple import config

# Get Django environment setting with None as default
ENV = config("DJANGO_ENV", default=None)

# Validate that DJANGO_ENV is set
if ENV is None:
    raise Exception("DJANGO_ENV environment variable is not set")

# Import settings based on environment
if ENV == "development":
    from .development import *  # noqa: F403
elif ENV == "production":
    from .production import *  # noqa: F403
else:
    # Raise error if ENV value is not one of the allowed options
    raise Exception(
        "Please define the DJANGO_ENV mode as development, production, or testing"
    )
