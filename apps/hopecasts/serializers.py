from rest_framework import serializers
from .models import Hopecast, HopecastCategory

class HopecastCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HopecastCategory
        fields = ('id', 'name', 'slug')

class HopecastSerializer(serializers.ModelSerializer):
    category_details = HopecastCategorySerializer(source='categories', many=True, read_only=True)
    
    class Meta:
        model = Hopecast
        fields = ('id', 'title', 'mp4_link', 'categories', 'category_details', 'created_at', 'updated_at')
        extra_kwargs = {
            'categories': {'write_only': True}
        }
