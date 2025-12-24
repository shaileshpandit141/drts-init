from envconfig import config

# Celery Configuration Settings
CELERY_BROKER_URL = config.CELERY_BROKER_URL

# Where results are stored
CELERY_RESULT_BACKEND = config.CELERY_RESULT_BACKEND

# Recommended settings
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

# Task time limits (avoid runaway tasks)
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 mins
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60
