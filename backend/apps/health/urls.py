from django.urls import path
from apps.health.views import HealthCheckView

urlpatterns = [
    path("", HealthCheckView.as_view(), name="health-check"),
]
