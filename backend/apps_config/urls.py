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
from rest_core.django.views import url_404_apiview

from .views import IndexTemplateView

# Built-in URL Configurations
urlpatterns = [
    path("", IndexTemplateView.as_view(), name="index"),
    path(
        "favicon.ico",
        RedirectView.as_view(
            url="/static/favicon.ico",
            permanent=True,
        ),
    ),
    path("admin/", admin.site.urls, name="admin"),
]

# User-Defined URL Configurations
# ===============================
# Auth related URLs Configurations
urlpatterns += [
    path("api/v1/auth/", include(("apps.accounts.urls", "accounts"))),
    path("api/v1/auth/", include(("apps.google_auth.urls", "google_auth"))),
]

# API related URLs Configurations
urlpatterns += []

# Configure custom error handling
handler404 = url_404_apiview  # noqa: F811

# Enable serving of user-uploaded media files
if settings.DEBUG:
    # Drf session authentication
    urlpatterns += [
        path("", include("rest_framework.urls")),
    ]

    # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
