from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HopecastViewSet, HopecastCategoryViewSet

router = DefaultRouter()
router.register(r'categories', HopecastCategoryViewSet, basename='hopecast-category')
router.register(r'', HopecastViewSet, basename='hopecast')

urlpatterns = [
    path('', include(router.urls)),
]
