from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Local development settings: run Celery tasks synchronously
CELERY_TASK_ALWAYS_EAGER = True
CELERY_RESULT_BACKEND = None
