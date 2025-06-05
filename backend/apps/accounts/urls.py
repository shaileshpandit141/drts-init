"""
Django Accounts App URL Configuration

This module defines URL patterns for the accounts application, handling user authentication,
registration, password management, and profile data. All paths are prefixed with /accounts/
when included in the main URLs.
"""

from accounts.views.deactivation_views import AccountDeactivationView
from accounts.views.password_views import (
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from accounts.views.signin_views import (
    TokenBlockView,
    TokenRefreshView,
    TokenRetriveView,
)
from accounts.views.signup_views import (
    AccountVerificationConfirmView,
    AccountVerificationView,
    SignupView,
)
from accounts.views.user_profile_views import UserProfileView
from django.urls import path

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path(
        "account-verification/",
        AccountVerificationView.as_view(),
        name="account-verification",
    ),
    path(
        "account-verification/confirm/",
        AccountVerificationConfirmView.as_view(),
        name="account-verification-confirm",
    ),
    path("token/", TokenRetriveView.as_view(), name="token-retrive"),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),
    path("token/block/", TokenBlockView.as_view(), name="token-block"),
    path("password/change/", PasswordChangeView.as_view(), name="password-change"),
    path("password/reset/", PasswordResetView.as_view(), name="password-reset"),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "account-deactivation/",
        AccountDeactivationView.as_view(),
        name="account-deactivation",
    ),
    path("user/", UserProfileView.as_view(), name="user-profile"),
]
