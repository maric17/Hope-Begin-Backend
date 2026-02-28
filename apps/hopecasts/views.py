from rest_framework import viewsets, permissions
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
        # Anyone can view hopecasts
        return [permissions.AllowAny()]
