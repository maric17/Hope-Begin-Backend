from rest_framework import serializers
from .models import HopeStory

class HopeStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HopeStory
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class PublicHopeStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HopeStory
        fields = ('id', 'full_name', 'occupation', 'testimonial', 'photo', 'created_at')
        read_only_fields = ('id', 'created_at')

class HopeStoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HopeStory
        fields = ('full_name', 'occupation', 'testimonial', 'photo')

    def validate_testimonial(self, value):
        word_count = len(value.split())
        if word_count > 200:
            raise serializers.ValidationError("Testimonial must be 200 words or less.")
        return value
