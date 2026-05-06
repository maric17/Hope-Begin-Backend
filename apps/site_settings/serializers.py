from rest_framework import serializers
from .models import PopoutSettings, PopoutItem, JourneyContent

class PopoutItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopoutItem
        fields = ['id', 'message', 'button_text', 'link', 'is_active']

class PopoutSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopoutSettings
        fields = ['id', 'is_enabled', 'interval_seconds']

class JourneyContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneyContent
        fields = ['id', 'title', 'description', 'video_embed_url', 'updated_at']
