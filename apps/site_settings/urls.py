from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PublicPopoutView, 
    PopoutSettingsViewSet, 
    PopoutItemViewSet,
    JourneyContentViewSet
)

router = DefaultRouter()
router.register(r'settings', PopoutSettingsViewSet, basename='popout-settings')
router.register(r'items', PopoutItemViewSet, basename='popout-items')
router.register(r'journey-content', JourneyContentViewSet, basename='journey-content')

urlpatterns = [
    path('public/', PublicPopoutView.as_view(), name='public-popouts'),
    path('', include(router.urls)),
]
