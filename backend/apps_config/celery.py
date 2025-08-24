import os

from celery import Celery

# Set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps_config.settings")

app = Celery("apps_config")

# Load settings from Django, namespace CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")  # type: ignore[arg-type]


# Autodiscover tasks from all installed apps
app.autodiscover_tasks()  # type: ignore[attr-defined]
