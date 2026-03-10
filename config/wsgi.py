import os

from django.core.wsgi import get_wsgi_application
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Determine settings module based on ENVIRONMENT variable
django_env = env('ENVIRONMENT', default='production')
settings_module = 'config.settings.prod' if django_env == 'production' else 'config.settings.dev'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
