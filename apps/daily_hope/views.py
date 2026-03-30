from rest_framework import viewsets, permissions, status, pagination, filters
from rest_framework.response import Response
from .models import HopeJourney, HopefulBeginningCompletion
from .serializers import HopeJourneySerializer
from rest_framework.views import APIView

class HopeJourneyPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class HopeJourneyViewSet(viewsets.ModelViewSet):
    queryset = HopeJourney.objects.all()
    serializer_class = HopeJourneySerializer
    pagination_class = HopeJourneyPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']

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
            subscriber = serializer.save()
            
            # Send Day 1 immediately
            from .tasks import send_welcome_and_day_one
            send_welcome_and_day_one.delay(subscriber.id)

            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            response.data['message'] = "Welcome to your 21-day Hope Journey! Check your email for Day 1."
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HopefulBeginningCompletionView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        HopefulBeginningCompletion.objects.create()
        return Response({"message": "Hopeful Beginning completion recorded."}, status=status.HTTP_201_CREATED)
