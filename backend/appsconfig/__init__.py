from dotenv import load_dotenv
from .celery import app as celery_app

# Load .env file.
load_dotenv()

__all__ = ("celery_app",)
