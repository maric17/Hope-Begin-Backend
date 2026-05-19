import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev') # Assuming dev settings
django.setup()

from apps.site_settings.models import PopoutSettings, PopoutItem

# Create default settings
if not PopoutSettings.objects.exists():
    PopoutSettings.objects.create(is_enabled=True, interval_seconds=15)
    print("Created PopoutSettings")

# Initial items
items = [
    {
        "message": "Someone just gave hope",
        "button_text": "JOIN",
        "link": "/be-carrier"
    },
    {
        "message": "Someone has been prayed for",
        "button_text": "PRAY",
        "link": "/prayers"
    },
    {
        "message": "Someone listened to hope",
        "button_text": "LISTEN",
        "link": "/hopecasts"
    },
    {
        "message": "Someone supported hope",
        "button_text": "SUPPORT",
        "link": "/give-hope"
    },
    {
        "message": "Someone journeyed with hope",
        "button_text": "JOURNEY",
        "link": "/daily-hope"
    }
]

for item in items:
    PopoutItem.objects.get_or_create(
        message=item["message"],
        button_text=item["button_text"],
        link=item["link"]
    )
    print(f"Ensured item: {item['message']}")
