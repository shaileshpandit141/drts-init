import logging
from typing import TYPE_CHECKING, Literal, cast

from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

if TYPE_CHECKING:
    from .models import User

logger = logging.getLogger(__name__)


class IsUserAccountVerified(BasePermission):
    """Permission class that checks if a user is verified."""

    def has_permission(
        self,
        request: Request,
        view: APIView,
    ) -> Literal[True]:
        """Check if the user is verified or a superuser."""
        user: User | AnonymousUser = cast("User | AnonymousUser", request.user)

        if isinstance(user, AnonymousUser):
            log_war: str = (
                f"Anonymous user attempted to access {request.method} {request.path}."
            )
            logger.warning(log_war)
            raise PermissionDenied(
                {
                    "detail": "You must be logged in to access this resource.",
                    "code": "not_authenticated",
                }
            )

        if not user.is_authenticated:
            log_msg = (
                f"Unauthenticated user {user.email} attempted to access "
                f"{request.method} {request.path}."
            )
            logger.warning(log_msg)
            raise PermissionDenied(
                {
                    "detail": "You must be sign in to access this resource.",
                    "code": "not_authenticated",
                }
            )

        if user.is_superuser:
            log_info: str = f"Superuser {user.email} authenticated successfully for {request.method} {request.path}."
            logger.info(log_info)
            return True

        if not user.is_verified:
            log_warx: str = f"Unverified user {user.email} attempted to access {request.method} {request.path}."
            logger.warning(log_warx)
            raise PermissionDenied(
                {
                    "detail": "Please verify your account to access this resource.",
                    "code": "unverified_account",
                }
            )

        # Log successful verification
        log_infox: str = f"Verified user {user.email} successfully accessed {request.method} {request.path}."
        logger.info(log_infox)
        return True
