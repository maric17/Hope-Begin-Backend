from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HopeStoryViewSet

router = DefaultRouter()
router.register(r'', HopeStoryViewSet, basename='hope-story')

urlpatterns = [
    path('', include(router.urls)),
]
