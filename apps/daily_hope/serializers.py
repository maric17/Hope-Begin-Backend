from rest_framework import serializers
from .models import HopeJourney

class HopeJourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = HopeJourney
        fields = ('id', 'first_name', 'last_name', 'email', 'current_day', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
