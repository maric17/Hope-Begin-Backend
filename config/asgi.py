import os

from django.core.asgi import get_asgi_application

# Default to dev settings if DJANGO_SETTINGS_MODULE is not set
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

application = get_asgi_application()
