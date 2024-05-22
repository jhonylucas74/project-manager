from django.forms import ValidationError
from .models import CustomUser
from .serializers import SignUpSerializer, CustomUserSerializer, SignInSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

class UserSignUp(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		serializer = SignUpSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		
		try:
			validate_password(serializer.validated_data["password"])
		except ValidationError as e:
			return Response({ 'password': e.messages }, status=status.HTTP_400_BAD_REQUEST)

		user = CustomUser.objects.create_user(**serializer.validated_data)
		refresh = RefreshToken.for_user(user)

		return Response({
			"refresh": str(refresh),
			"access": str(refresh.access_token),
			"user": CustomUserSerializer(user).data
		})

class UserSignIn(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		serializer = SignInSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		email = serializer.validated_data.get('email')
		password = serializer.validated_data.get('password')

		user = authenticate(request, email=email, password=password)

		if user is None:
			return Response({ 'error': 'Invalid credentials' }, status=status.HTTP_400_BAD_REQUEST)
		
		refresh = RefreshToken.for_user(user)

		return Response({
			"refresh": str(refresh),
			"access": str(refresh.access_token),
			"user": CustomUserSerializer(user).data
		})

class GetMe(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		return Response(CustomUserSerializer(request.user).data)
