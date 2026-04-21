from rest_framework import serializers
from .models import HopeJourney

class HopeJourneySerializer(serializers.ModelSerializer):
    website = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = HopeJourney
        fields = ('id', 'first_name', 'last_name', 'email', 'current_day', 'created_at', 'updated_at', 'website')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate(self, data):
        if data.get('website'):
            raise serializers.ValidationError("Anti-spam: Bot detected.")
        # Remove website so it doesn't get passed to the model
        data.pop('website', None)
        return data
