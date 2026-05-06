from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrayerViewSet, PrayerResponseViewSet, OrganizationViewSet

router = DefaultRouter()
router.register(r'requests', PrayerViewSet, basename='prayer-request')
router.register(r'responses', PrayerResponseViewSet, basename='prayer-response')
router.register(r'organizations', OrganizationViewSet, basename='organization')

urlpatterns = [
    path('', include(router.urls)),
]
