from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    AdminRegistrationView, 
    MyTokenObtainPairView, 
    RegistrationView,
    UserViewSet,
    ForgotPasswordView,
    ResetPasswordView,
    LogoutView,
    CarrierApplicationView
)

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('register/carrier/', CarrierApplicationView.as_view(), name='carrier_application'),
    path('register/admin/', AdminRegistrationView.as_view(), name='admin_registration'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('', include(router.urls)),
]
