import hashlib

from rest_framework.throttling import SimpleRateThrottle


class AuthUserRateThrottle(SimpleRateThrottle):
    scope = "auth"  # Must match the key in settings' DEFAULT_THROTTLE_RATES

    def get_cache_key(self, request, view) -> str:
        """
        Generate a cache key unique to each device on the same network.
        Use a combination of IP and device-specific identifier.
        """
        router_ip = self.get_ident(request)  # Uses IP from request.META['REMOTE_ADDR']

        if request.user and request.user.is_authenticated:
            # Use user ID for authenticated users
            device_id = f"user_{request.user.id}"
        else:
            # Hash of User-Agent header for anonymous users
            user_agent = request.META.get("HTTP_USER_AGENT", "unknown_device")
            device_id = hashlib.md5(user_agent.encode("utf-8")).hexdigest()

        # Cache key combines IP and device ID
        return f"throttle_{router_ip}_{device_id}"
