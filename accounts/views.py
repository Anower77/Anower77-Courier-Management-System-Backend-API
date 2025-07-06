from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "success": True,
                "statusCode": 201,
                "message": "User registered successfully",
                "data": UserSerializer(user).data
            }, status=201)
        return Response({
            "success": False,
            "message": "Validation error occurred.",
            "errorDetails": serializer.errors
        }, status=400)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                "success": True,
                "statusCode": 200,
                "message": "Login successful",
                "data": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }
            })
        return Response({
            "success": False,
            "statusCode": 401,
            "message": "Invalid credentials",
            "data": None
        }, status=401)
