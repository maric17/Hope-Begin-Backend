from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import HopeJourney
from .serializers import HopeJourneySerializer

class HopeJourneyViewSet(viewsets.ModelViewSet):
    queryset = HopeJourney.objects.all()
    serializer_class = HopeJourneySerializer

    def get_permissions(self):
        # Anyone can join the journey (create)
        if self.action == 'create':
            return [permissions.AllowAny()]
        # Only admin can list, retrieve, update or delete subscriptions
        return [permissions.IsAdminUser()]

    def create(self, request, *args, **kwargs):
        # Standardize response message
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            response.message = "Welcome to your 21-day Hope Journey!"
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
