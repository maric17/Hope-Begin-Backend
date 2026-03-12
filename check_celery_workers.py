from celery import Celery
import os
from pathlib import Path
import environ

BASE_DIR = Path(r"c:\RepoOutside\hopebeginbackend")
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

django_env = env('ENVIRONMENT', default='production')
settings_module = 'config.settings.prod' if django_env == 'production' else 'config.settings.dev'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

from config.celery import app

i = app.control.inspect()
print("Ping active workers:")
print(i.ping())

print("\nActive tasks:")
print(i.active())

print("\nRegistered tasks:")
print(i.registered())

print("\nStats:")
stats = i.stats()
if stats:
    for worker, data in stats.items():
        print(f"Worker {worker} processed tasks: {data.get('total', {})}")
else:
    print("No workers found")
