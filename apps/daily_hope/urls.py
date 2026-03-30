from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HopeJourneyViewSet, HopefulBeginningCompletionView

router = DefaultRouter()
router.register(r'journeys', HopeJourneyViewSet, basename='hope-journey')

urlpatterns = [
    path('hopeful-beginning-complete/', HopefulBeginningCompletionView.as_view(), name='hopeful_beginning_complete'),
    path('', include(router.urls)),
]
