from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Hopecast, HopecastCategory, HopecastPlayLog
from .serializers import HopecastSerializer, HopecastCategorySerializer

class HopecastPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

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
    pagination_class = HopecastPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ('categories',)
    search_fields = ('title', 'name', 'verse')
    ordering_fields = ('created_at', 'play_count', 'title')
    ordering = ('-created_at',)

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
        HopecastPlayLog.objects.create(hopecast=hopecast)
        
        response = Response(self.get_serializer(hopecast).data)
        response.message = f"Play count incremented for: {hopecast.title}"
        return response
