from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DonationViewSet
from .views_stripe import CreateCheckoutSessionView, stripe_webhook

router = DefaultRouter()
router.register(r'', DonationViewSet)

urlpatterns = [
    path('checkout/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
    path('', include(router.urls)),
]
