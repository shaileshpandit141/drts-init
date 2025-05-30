import hashlib

from rest_framework.throttling import SimpleRateThrottle


class AuthUserRateThrottle(SimpleRateThrottle):
    """
    Throttle requests based on user authentication status and device.

    This throttle generates a cache key that is specific to each view, request method,
    request IP, and device identifier. For authenticated users, the device is identified
    by the user's ID; for unauthenticated users, it uses a hashed user agent.
    """

    # Define the scope for this throttle class
    # This scope should match the key in settings DEFAULT_THROTTLE_RATES
    scope = "auth"

    def get_cache_key(self, request, view) -> str:
        """
        Generate a unique cache key for throttling.

        The cache key is constructed using:
          - The fully qualified view name (module and class name)
          - The HTTP request method
          - The router IP address derived from the request
          - A device ID, which is based on the user authentication status:
              * For authenticated users: "user_{user_id}"
              * For unauthenticated users: MD5 hash of the HTTP_USER_AGENT

        Parameters:
          request: The incoming HTTP request.
          view: The view handling the request.

        Returns:
          A string representing the unique cache key.
        """
        # Get the router IP address from the request
        router_ip = self.get_ident(request)

        # Determine device ID based on user authentication status
        if request.user and request.user.is_authenticated:
            device_id = f"user_{request.user.id}"
        else:
            user_agent = request.META.get("HTTP_USER_AGENT", "unknown_device")
            device_id = hashlib.md5(user_agent.encode("utf-8")).hexdigest()

        # Include view name for better cache key as for view-specific throttling
        view_id = f"{view.__class__.__module__}.{view.__class__.__name__}"

        # Cache key combines view ID, request method, router IP, and device ID
        return f"throttle_{view_id}_{request.method}_{router_ip}_{device_id}"
