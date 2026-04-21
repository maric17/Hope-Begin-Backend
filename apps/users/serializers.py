from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['role'] = user.role
        token['email'] = user.email
        token['is_approved'] = user.is_approved
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add extra responses
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'username': self.user.username,
            'role': self.user.role,
            'is_approved': self.user.is_approved,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
        }
        return data

class UserSerializer(serializers.ModelSerializer):
    prayer_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'role', 'is_approved', 
            'first_name', 'last_name', 'phone', 'church_community', 
            'carrier_reason', 'agreed_to_guidelines', 'date_joined',
            'prayer_count'
        )
        read_only_fields = ('id', 'role', 'is_approved', 'date_joined', 'prayer_count')

    def get_prayer_count(self, obj):
        return obj.assigned_prayers.count()

class AdminUserSerializer(serializers.ModelSerializer):
    prayer_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'role', 'is_approved', 
            'first_name', 'last_name', 'phone', 'church_community', 
            'carrier_reason', 'agreed_to_guidelines', 'date_joined',
            'prayer_count'
        )
        read_only_fields = ('id', 'date_joined', 'prayer_count')

    def get_prayer_count(self, obj):
        return obj.assigned_prayers.count()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role='user',
            is_approved=False  # Registration must be approved by admin
        )
        return user

class AdminRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role='admin',
            is_staff=True,
            is_approved=True  # Admin users are pre-approved for now
        )
        return user

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

class ResetPasswordSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            uid = force_str(urlsafe_base64_decode(attrs['uidb64']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid token or user ID.")

        if not default_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError("Invalid or expired token.")

        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
class CarrierApplicationSerializer(serializers.ModelSerializer):
    website = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 
            'phone', 'church_community', 'carrier_reason', 'agreed_to_guidelines',
            'website'
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'carrier_reason': {'required': True},
            'agreed_to_guidelines': {'required': True}
        }

    def validate_agreed_to_guidelines(self, value):
        if not value:
            raise serializers.ValidationError("You must agree to the guidelines to apply.")
        return value

    def validate(self, data):
        if data.get('website'):
            raise serializers.ValidationError("Anti-spam: Bot detected.")
        return data

    def create(self, validated_data):
        # Create a user without a password (it will be set after approval)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=get_random_string(32),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            church_community=validated_data.get('church_community', ''),
            carrier_reason=validated_data.get('carrier_reason', ''),
            agreed_to_guidelines=validated_data.get('agreed_to_guidelines', False),
            role='carrier',
            is_approved=False
        )
        return user
