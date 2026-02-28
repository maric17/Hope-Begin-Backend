from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AdminRegistrationView, MyTokenObtainPairView

urlpatterns = [
    path('register/admin/', AdminRegistrationView.as_view(), name='admin_registration'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
