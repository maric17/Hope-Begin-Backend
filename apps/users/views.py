from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
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
            response.message = "Carrier application submitted. Pending admin approval."
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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    filterset_fields = ['role', 'is_approved']
    
    def get_serializer_class(self):
        if self.request.user.role == 'admin':
            return AdminUserSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.IsAdminUser()]
        if self.action in ['retrieve', 'partial_update', 'update']:
            return [IsOwnerOrAdmin()]
        if self.action in ['me', 'my_profile']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

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
        user.save()

        # If it's a carrier, send the "Set Password" email
        if user.role == 'carrier':
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            
            # The URL to set password (frontend URL)
            set_password_url = f"http://localhost:3000/reset-password?uid={uidb64}&token={token}"
            
            send_mail(
                "Welcome to Hope Begins - Set Your Password",
                f"Your application as a Hope Carrier has been approved! Use this link to set your password and access your dashboard: {set_password_url}",
                "noreply@hopebegins.org",
                [user.email],
                fail_silently=False,
            )
            message = "Carrier approved and invitation email sent."
        else:
            message = "User approved successfully."

        response = Response(UserSerializer(user).data)
        response.message = message
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
            reset_url = f"http://localhost:3000/reset-password?uid={uidb64}&token={token}"
            
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
