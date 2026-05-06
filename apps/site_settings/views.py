from rest_framework import viewsets, permissions, views
from rest_framework.response import Response
from .models import PopoutSettings, PopoutItem, JourneyContent
from .serializers import PopoutSettingsSerializer, PopoutItemSerializer, JourneyContentSerializer

class PublicPopoutView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        settings = PopoutSettings.objects.first()
        if not settings:
            settings = PopoutSettings.objects.create(is_enabled=True, interval_seconds=15)
        
        items = PopoutItem.objects.filter(is_active=True)
        
        return Response({
            "is_enabled": settings.is_enabled,
            "interval_seconds": settings.interval_seconds,
            "items": PopoutItemSerializer(items, many=True).data
        })

class PopoutSettingsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = PopoutSettings.objects.all()
    serializer_class = PopoutSettingsSerializer

class PopoutItemViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = PopoutItem.objects.all().order_by('-created_at')
    serializer_class = PopoutItemSerializer

class JourneyContentViewSet(viewsets.ModelViewSet):
    queryset = JourneyContent.objects.all()
    serializer_class = JourneyContentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def list(self, request, *args, **kwargs):
        instance = JourneyContent.objects.first()
        if not instance:
            instance = JourneyContent.objects.create()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
