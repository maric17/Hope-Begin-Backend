import os

from django.core.wsgi import get_wsgi_application

# Default to dev settings if DJANGO_SETTINGS_MODULE is not set
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

application = get_wsgi_application()
