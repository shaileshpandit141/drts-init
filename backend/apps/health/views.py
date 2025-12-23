from rest_framework.request import Request
from django.core.cache import cache
from django.db import connections
from django.db.utils import OperationalError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.health.throttles import HealthCheckThrottle

HEALTH_CACHE_KEY = "system_health_status"
HEALTHY_TTL = 30  # seconds
UNHEALTHY_TTL = 5  # seconds


class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = [HealthCheckThrottle]

    def get(self, request: Request) -> Response:
        cached_health = cache.get(HEALTH_CACHE_KEY)
        if cached_health:
            return Response(
                cached_health,
                status=(
                    status.HTTP_200_OK
                    if cached_health["status"] == "ok"
                    else status.HTTP_503_SERVICE_UNAVAILABLE
                ),
            )

        health_data = {"status": "ok"}

        try:
            connections["default"].cursor()
        except OperationalError:
            health_data["status"] = "unhealthy"

        ttl = HEALTHY_TTL if health_data["status"] == "ok" else UNHEALTHY_TTL
        cache.set(HEALTH_CACHE_KEY, health_data, ttl)

        return Response(
            health_data,
            status=(
                status.HTTP_200_OK
                if health_data["status"] == "ok"
                else status.HTTP_503_SERVICE_UNAVAILABLE
            ),
        )
