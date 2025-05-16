"""
URL Configuration for Django Backend Project

This module defines the URL patterns and routing configuration for the core Django application.
It maps URLs to their corresponding views and configures static file serving and error handling.
"""

from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

from apps.google_auth import urls as google_auth_urls
from apps.user_auth import urls as users_auth_urls

from .views import IndexTemplateView, custom_404_apiview

# Main URL patterns defining route-to-view mappings
urlpatterns = [
    # Served the index page
    path("", IndexTemplateView.as_view(), name="index"),
    # Django admin interface accessible at /admin
    path("admin/", admin.site.urls, name="admin"),
    # # Redirect /favicon.ico requests to the static file location of the favicon
    path(
        "favicon.ico", RedirectView.as_view(url="/static/favicon.ico", permanent=True)
    ),
    # User authentication URLs under /api/v1/auth
    path("api/v1/auth/", include((users_auth_urls, "user_auth"))),
    path("api/v1/auth/", include((google_auth_urls, "google_auth"))),
]

# Configure custom error handling
handler404 = custom_404_apiview

# Enable serving of user-uploaded media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
