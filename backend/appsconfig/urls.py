"""URL Configuration for Django Backend Project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from .views import index_view, get_favicon

# Built-in URL Configurations
urlpatterns = [
    path("", index_view, name="index"),
    path("favicon.ico/", get_favicon()),
    path("admin/", admin.site.urls, name="admin"),
]

# User-Defined URL Configurations
# ===============================

# Auth related URLs Configurations
urlpatterns += [
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/auth/", include("apps.google_auth.urls")),
]

# API related URLs Configurations
urlpatterns += []


# Drf session authentication
if settings.DEBUG:
    urlpatterns += [
        path("", include("rest_framework.urls")),
    ]

    # Serve media files during development
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
