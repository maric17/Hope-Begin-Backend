from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Prayer, PrayerResponse
from .serializers import PrayerSerializer, AdminPrayerSerializer, PrayerResponseSerializer
from apps.users.permissions import IsApproved

class PrayerViewSet(viewsets.ModelViewSet):
    queryset = Prayer.objects.all()
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_class(self):
        # Admin gets full control serializer
        if self.request.user.is_authenticated and self.request.user.role == 'admin':
            return AdminPrayerSerializer
        # Public only gets the submission serializer
        return PrayerSerializer

    def get_permissions(self):
        # Allow anyone to submit a prayer
        if self.action == 'create':
            return [permissions.AllowAny()]
        # List and other management requires approval
        if self.action in ['list', 'retrieve', 'partial_update', 'update', 'destroy', 'assign', 'mark_prayed']:
            return [permissions.IsAuthenticated(), IsApproved()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        # If user is authenticated, link the prayer to them
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def assign(self, request, pk=None):
        prayer = self.get_object()
        carrier_id = request.data.get('carrier_id')
        if carrier_id:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                carrier = User.objects.get(id=carrier_id, role='carrier')
                prayer.assigned_to = carrier
                prayer.status = 'ASSIGNED'
                prayer.save()
                response = Response(AdminPrayerSerializer(prayer).data)
                response.message = f"Prayer assigned to {carrier.email} successfully."
                return response
            except User.DoesNotExist:
                return Response({"error": "Carrier not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "carrier_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsApproved])
    def mark_prayed(self, request, pk=None):
        prayer = self.get_object()
        prayer.status = 'PRAYED'
        prayer.save()
        response = Response(self.get_serializer(prayer).data)
        response.message = "Prayer marked as prayed."
        return response

class PrayerResponseViewSet(viewsets.ModelViewSet):
    queryset = PrayerResponse.objects.all()
    serializer_class = PrayerResponseSerializer
    permission_classes = [permissions.IsAuthenticated, IsApproved]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
