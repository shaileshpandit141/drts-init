"""ASGI Configuration for Apps Config Project."""

import os

# Import Django's ASGI handler
from django.core.asgi import get_asgi_application

# Configure Django settings module path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appsconfig.settings")

# Create ASGI application instance
application = get_asgi_application()
