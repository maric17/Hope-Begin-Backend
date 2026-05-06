from rest_framework import serializers
from .models import PopoutSettings, PopoutItem

class PopoutItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopoutItem
        fields = ['id', 'message', 'button_text', 'link', 'is_active']

class PopoutSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopoutSettings
        fields = ['is_enabled', 'interval_seconds']
