from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum, Count
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions, viewsets, pagination, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.prayers.models import Prayer
from apps.hopecasts.models import Hopecast
from apps.prayers.serializers import PrayerSerializer
from .serializers import (
    AdminRegistrationSerializer, 
    MyTokenObtainPairSerializer, 
    UserRegistrationSerializer,
    UserSerializer,
    AdminUserSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    CarrierApplicationSerializer
)
from .permissions import IsOwnerOrAdmin

User = get_user_model()

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = Response(None, status=status.HTTP_205_RESET_CONTENT)
            response.message = "Logged out successfully."
            return response
        except Exception:
            return Response(
                {"error": "Invalid token or token already blacklisted."},
                status=status.HTTP_400_BAD_REQUEST
            )

class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response = Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            response.message = "Registration successful. Pending admin approval."
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CarrierApplicationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = CarrierApplicationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response = Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            response.message = "Your application is being reviewed. If approved, we will send a temporary password to your email."
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminRegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)  # In production, restrict this.

    def post(self, request):
        serializer = AdminRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response = Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            response.message = "Admin registered successfully."
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().annotate(prayer_count=Count('assigned_prayers'))
    serializer_class = UserSerializer
    pagination_class = UserPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email']
    filterset_fields = ['role', 'is_approved']
    ordering_fields = ['first_name', 'last_name', 'email', 'date_joined', 'prayer_count']
    ordering = ['-date_joined']
    
    def get_serializer_class(self):
        if self.request.user.role == 'admin':
            return AdminUserSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.IsAdminUser()]
        if self.action in ['retrieve', 'partial_update', 'update']:
            return [IsOwnerOrAdmin()]
        if self.action in ['me', 'my_profile', 'overview']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def overview(self, request):
        # 1. Total Prayers
        total_prayers = Prayer.objects.count()
        
        # 2. Pending (New) Prayers
        pending_prayers = Prayer.objects.filter(status='NEW').count()
        
        # 3. Approved Hope Carriers
        total_carriers = User.objects.filter(role='carrier', is_approved=True).count()
        
        # 4. Total HopeCast Plays
        total_hopecast_plays = Hopecast.objects.aggregate(total=Sum('play_count'))['total'] or 0
        
        # 5. Recent Prayer Requests (Top 5)
        recent_prayers = Prayer.objects.all().order_by('-created_at')[:5]
        recent_prayers_data = PrayerSerializer(recent_prayers, many=True).data

        # 6. Total registered users
        total_users = User.objects.count()

        data = {
            "total_prayers": total_prayers,
            "pending_prayers": pending_prayers,
            "total_carriers": total_carriers,
            "hopecast_plays": total_hopecast_plays,
            "total_users": total_users,
            "recent_prayers": recent_prayers_data
        }
        
        response = Response(data)
        response.message = "Dashboard overview data retrieved successfully."
        return response

    @action(detail=False, methods=['get', 'patch'], url_path='me')
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        user = self.get_object()
        user.is_approved = True
        
        # If it's a carrier, generate a temporary password and send email
        if user.role == 'carrier':
            temp_password = get_random_string(12)
            user.set_password(temp_password)
            user.save()
            
            login_url = f"{settings.FRONTEND_URL}/login/carrier"
            
            subject = "Welcome to Hope Begins - Your Application is Approved!"
            message = (
                f"Your application as a Hope Carrier has been approved!\n\n"
                f"You can now access your dashboard using the following credentials:\n"
                f"Username: {user.email}\n"
                f"Temporary Password: {temp_password}\n\n"
                f"Login here: {login_url}\n\n"
                "Please change your password after your first login for security purposes.\n\n"
                "Thank you for standing in the gap with us."
            )
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            message_response = "Carrier approved and credentials email sent."
        else:
            user.save()
            message_response = "User approved successfully."

        response = Response(UserSerializer(user).data)
        response.message = message_response
        return response

class ForgotPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Reset URL (frontend URL)
            reset_url = f"{settings.FRONTEND_URL}/reset-password?uid={uidb64}&token={token}"
            
            send_mail(
                "Password Reset Request",
                f"Use this link to reset your password: {reset_url}",
                "noreply@hopebegins.org",
                [email],
                fail_silently=False,
            )
            response = Response(None)
            response.message = "Password reset link sent to email."
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(None)
            response.message = "Password has been reset successfully."
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
