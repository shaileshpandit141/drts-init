from rest_framework.throttling import SimpleRateThrottle
from rest_framework.request import Request
from rest_framework.views import APIView


class HealthCheckThrottle(SimpleRateThrottle):
    """Docstring for HealthCheckThrottle."""

    scope = "health"

    def get_cache_key(self, request: Request, view: APIView) -> str | None:
        # Throttle by IP (safe for public endpoint)
        ip = self.get_ident(request)

        # Don't throttle internal IPs
        if ip.startswith("10.") or ip.startswith("192.168."):
            return None  # no throttle

        # Otherwise, use the IP as the cache key
        return ip
