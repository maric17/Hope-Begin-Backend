from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import AdminRegistrationSerializer, MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class AdminRegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)  # Allow anyone to register as an admin for now, or you might want to restrict this later.

    def post(self, request):
        serializer = AdminRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
