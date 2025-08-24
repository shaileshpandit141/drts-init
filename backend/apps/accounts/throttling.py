import hashlib

from rest_framework.request import Request
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.views import APIView


class AuthUserRateThrottle(SimpleRateThrottle):
    """Throttle requests based on user authentication status and device."""

    # Define the scope for this throttle class
    # This scope should match the key in settings DEFAULT_THROTTLE_RATES
    scope = "auth"

    def get_cache_key(self, request: Request, view: APIView) -> str:
        """Generate a unique cache key for throttling."""
        router_ip = self.get_ident(request)

        # Determine device ID based on user authentication status
        if request.user and request.user.is_authenticated:
            device_id = f"user_{request.user.id}"  # type: ignore[attr-defined]
        else:
            user_agent = request.META.get("HTTP_USER_AGENT", "unknown_device")
            device_id = hashlib.sha256(user_agent.encode("utf-8")).hexdigest()

        # Include view name for better cache key as for view-specific throttling
        view_id = f"{view.__class__.__module__}.{view.__class__.__name__}"

        # Cache key combines view ID, request method, router IP, and device ID
        return f"throttle_{view_id}_{request.method}_{router_ip}_{device_id}"
