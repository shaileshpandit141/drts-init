import logging
from typing import Literal

from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

logger = logging.getLogger(__name__)


class IsUserAccountVerified(BasePermission):
    """Permission class that checks if a user is verified."""

    def has_permission(self, request, view) -> Literal[True]:
        """Check if the user is verified or a superuser."""

        # Allow superusers unconditional access
        if request.user.is_superuser:
            logger.info(
                f"Superuser {request.user.username or request.user.email} authenticated successfully "
                f"for {request.method} {request.path}."
            )
            return True

        # Check if the user's account is verified
        if not getattr(request.user, "is_verified", False):
            logger.warning(
                f"Unverified user {request.user.id} ({request.user.email}) attempted to access "
                f"{request.method} {request.path}."
            )
            raise PermissionDenied(
                {
                    "message": "Account Verification Required",
                    "errors": [
                        {
                            "detail": "Please verify your account to access this resource.",
                            "code": "unverified_account",
                            "verification_status": False,
                            "user_id": request.user.id,
                            "user_email": request.user.email,
                        }
                    ],
                }
            )

        # Log successful verification
        logger.info(
            f"Verified user {request.user.username or request.user.email} successfully accessed "
            f"{request.method} {request.path}."
        )
        return True
