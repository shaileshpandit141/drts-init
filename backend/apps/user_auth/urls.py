"""
Django Accounts App URL Configuration

This module defines URL patterns for the accounts application, handling user authentication,
registration, password management, and profile data. All paths are prefixed with /accounts/
when included in the main URLs.
"""

from django.urls import path

from .views.change_password_views import ChangePasswordView
from .views.deactivate_account_views import DeactivateAccountView
from .views.forgot_password_views import ForgotPasswordConfirmView, ForgotPasswordView
from .views.signin_token_views import SigninTokenRefreshView, SigninTokenView
from .views.signout_views import SignoutView
from .views.signup_views import SignupView
from .views.user_info_views import UserInfoView
from .views.verify_account_views import VerifyAccountConfirmView, VerifyAccountView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("signin/token/", SigninTokenView.as_view(), name="signin_token"),
    path(
        "signin/token/refresh/",
        SigninTokenRefreshView.as_view(),
        name="signin_token_refresh",
    ),
    path("signout/", SignoutView.as_view(), name="sign_out"),
    path(
        "verify-user-account/", VerifyAccountView.as_view(), name="verify_user_account"
    ),
    path(
        "verify-user-account/confirm/",
        VerifyAccountConfirmView.as_view(),
        name="verify_user_account_confirm",
    ),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path(
        "forgot-password/confirm/",
        ForgotPasswordConfirmView.as_view(),
        name="forgot_password_confirm",
    ),
    path(
        "deactivate-account/",
        DeactivateAccountView.as_view(),
        name="deactivate_account",
    ),
    path("user/", UserInfoView.as_view(), name="user-info"),
]
