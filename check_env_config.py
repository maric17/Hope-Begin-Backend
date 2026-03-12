import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

print(f"OS ENVIRONMENT Variable: {os.environ.get('ENVIRONMENT')}")
print(f"Loaded from .env: {env('ENVIRONMENT', default='Not set')}")

django_env = env('ENVIRONMENT', default='production')
settings_module = 'config.settings.prod' if django_env == 'production' else 'config.settings.dev'
print(f"Calculated Settings Module: {settings_module}")

from django.conf import settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
django.setup()

print(f"Actual Configured EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"CELERY_TASK_ALWAYS_EAGER: {getattr(settings, 'CELERY_TASK_ALWAYS_EAGER', False)}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
