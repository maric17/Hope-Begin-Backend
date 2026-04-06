from django.apps import AppConfig

class PrayersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.prayers'

    def ready(self):
        import apps.prayers.signals
