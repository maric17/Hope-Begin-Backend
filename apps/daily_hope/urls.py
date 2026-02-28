from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HopeJourneyViewSet

router = DefaultRouter()
router.register(r'journeys', HopeJourneyViewSet, basename='hope-journey')

urlpatterns = [
    path('', include(router.urls)),
]
