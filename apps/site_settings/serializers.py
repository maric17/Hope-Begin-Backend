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


class JourneyPageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneyContent
        fields = [
            'id',
            'page_title',
            'page_subtitle',
            'steps',
            'welcome_section',
            'word_section',
            'prayer_section',
            'devotional_section',
            'next_steps_section',
            'crisis_section',
            'updated_at',
        ]

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        word_section = instance.word_section or {}

        legacy_updates = []
        title = word_section.get('title')
        description = word_section.get('description')
        video_embed_url = word_section.get('video_embed_url')

        if title and instance.title != title:
            instance.title = title
            legacy_updates.append('title')

        if description and instance.description != description:
            instance.description = description
            legacy_updates.append('description')

        if video_embed_url and instance.video_embed_url != video_embed_url:
            instance.video_embed_url = video_embed_url
            legacy_updates.append('video_embed_url')

        if legacy_updates:
            instance.save(update_fields=[*legacy_updates, 'updated_at'])

        return instance
