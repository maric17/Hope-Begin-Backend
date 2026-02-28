from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrayerViewSet, PrayerResponseViewSet

router = DefaultRouter()
router.register(r'requests', PrayerViewSet, basename='prayer-request')
router.register(r'responses', PrayerResponseViewSet, basename='prayer-response')

urlpatterns = [
    path('', include(router.urls)),
]
