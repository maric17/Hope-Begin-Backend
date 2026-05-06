from django.urls import path
from .views import AnalyticsView, ImpactAnalyticsView

urlpatterns = [
    path('', AnalyticsView.as_view(), name='analytics-overview'),
    path('impact/', ImpactAnalyticsView.as_view(), name='impact-analytics'),
]
