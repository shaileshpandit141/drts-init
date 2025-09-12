"""WSGI (Web Server Gateway Interface) Configuration."""

import os

from django.core.wsgi import get_wsgi_application

# Configure Django settings module path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Initialize WSGI application
application = get_wsgi_application()
