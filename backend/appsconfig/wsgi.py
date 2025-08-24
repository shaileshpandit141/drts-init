"""
WSGI (Web Server Gateway Interface) Configuration.

This module configures the WSGI application for the Django backend project.
It creates a WSGI callable named "application" that web servers can use
to communicate with the Django application.

Key components:
- Sets up the Django settings module in environment variables
- Creates the WSGI application object using Django"s get_wsgi_application()
"""

import os

from django.core.wsgi import get_wsgi_application

# Configure Django settings module path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Initialize WSGI application
application = get_wsgi_application()
