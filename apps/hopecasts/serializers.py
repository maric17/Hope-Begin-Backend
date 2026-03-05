from rest_framework import serializers
from .models import Hopecast, HopecastCategory

class HopecastCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HopecastCategory
        fields = ('id', 'name', 'slug')

class HopecastSerializer(serializers.ModelSerializer):
    category_details = HopecastCategorySerializer(source='categories', many=True, read_only=True)
    play_times = serializers.IntegerField(source='play_count', read_only=True)
    
    class Meta:
        model = Hopecast
        fields = ('id', 'title', 'name', 'verse', 'mp4_link', 'categories', 'category_details', 'play_times', 'created_at', 'updated_at')
        extra_kwargs = {
            'categories': {'write_only': True}
        }
