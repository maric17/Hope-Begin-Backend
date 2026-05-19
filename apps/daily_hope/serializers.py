from rest_framework import serializers
from .models import HopeJourney, EmailTemplate

class HopeJourneySerializer(serializers.ModelSerializer):
    website = serializers.CharField(required=False, allow_blank=True, write_only=True)
    last_name_honey = serializers.CharField(required=False, allow_blank=True, write_only=True)
    start_time = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model = HopeJourney
        fields = ('id', 'first_name', 'last_name', 'email', 'current_day', 'created_at', 'updated_at', 'website', 'last_name_honey', 'start_time')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate(self, data):
        from common.utils import validate_form_time
        
        # Honeypot checks
        if data.get('website') or data.get('last_name_honey'):
            raise serializers.ValidationError("Anti-spam: Bot detected.")
            
        # Time-based validation
        start_time = data.get('start_time')
        if not validate_form_time(start_time):
            raise serializers.ValidationError("Anti-spam: Form submitted too quickly.")
            
        # Remove fields so they don't get passed to the model
        data.pop('website', None)
        data.pop('last_name_honey', None)
        data.pop('start_time', None)
        return data


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = '__all__'
