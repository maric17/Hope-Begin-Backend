from rest_framework import serializers
from .models import Prayer, PrayerResponse
from django.contrib.auth import get_user_model

User = get_user_model()

class PrayerResponseSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = PrayerResponse
        fields = ('id', 'prayer', 'content', 'user', 'user_email', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')

class PrayerSerializer(serializers.ModelSerializer):
    responses = PrayerResponseSerializer(many=True, read_only=True)
    assigned_to_email = serializers.EmailField(source='assigned_to.email', read_only=True)
    
    # CamelCase fields for frontend compatibility
    isAnonymous = serializers.BooleanField(source='is_anonymous', required=False)
    shareFirstName = serializers.BooleanField(source='share_first_name', required=False)
    wantsFollowUp = serializers.BooleanField(source='wants_follow_up', required=False)
    website = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = Prayer
        fields = (
            'id', 'title', 'email', 'content', 'category', 
            'isAnonymous', 'shareFirstName', 'wantsFollowUp', 
            'status', 'assigned_to', 'assigned_to_email', 
            'user', 'created_at', 'updated_at', 'responses',
            'website'
        )
        read_only_fields = (
            'id', 'status', 'assigned_to', 'user', 
            'created_at', 'updated_at', 'responses'
        )

    def validate(self, data):
        if data.get('website'):
            raise serializers.ValidationError("Anti-spam: Bot detected.")
        # Remove website so it doesn't get passed to the model
        data.pop('website', None)
        return data

class AdminPrayerSerializer(serializers.ModelSerializer):
    responses = PrayerResponseSerializer(many=True, read_only=True)
    assigned_to_email = serializers.EmailField(source='assigned_to.email', read_only=True)
    
    # CamelCase fields for frontend compatibility
    isAnonymous = serializers.BooleanField(source='is_anonymous', required=False)
    shareFirstName = serializers.BooleanField(source='share_first_name', required=False)
    wantsFollowUp = serializers.BooleanField(source='wants_follow_up', required=False)

    class Meta:
        model = Prayer
        fields = (
            'id', 'title', 'email', 'content', 'category', 
            'isAnonymous', 'shareFirstName', 'wantsFollowUp', 
            'status', 'assigned_to', 'assigned_to_email', 
            'user', 'created_at', 'updated_at', 'responses'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'responses')
