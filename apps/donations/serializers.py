from rest_framework import serializers
from .models import Donation

class DonationSerializer(serializers.ModelSerializer):
    website = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = Donation
        fields = '__all__'

    def validate(self, data):
        if data.get('website'):
            raise serializers.ValidationError("Anti-spam: Bot detected.")
        # Remove website so it doesn't get passed to the model
        data.pop('website', None)
        return data
