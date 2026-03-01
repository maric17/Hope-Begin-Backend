from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Hopecast, HopecastCategory
from .serializers import HopecastSerializer, HopecastCategorySerializer

class HopecastCategoryViewSet(viewsets.ModelViewSet):
    queryset = HopecastCategory.objects.all()
    serializer_class = HopecastCategorySerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class HopecastViewSet(viewsets.ModelViewSet):
    queryset = Hopecast.objects.all()
    serializer_class = HopecastSerializer

    def get_permissions(self):
        # Only admin can add, edit, or delete hopecasts
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        # Anyone can view hopecasts or increment play times
        return [permissions.AllowAny()]

    @action(detail=True, methods=['post'], url_path='play')
    def increment_play_count(self, request, pk=None):
        hopecast = self.get_object()
        hopecast.play_count += 1
        hopecast.save()
        
        response = Response(self.get_serializer(hopecast).data)
        response.message = f"Play count incremented for: {hopecast.title}"
        return response
