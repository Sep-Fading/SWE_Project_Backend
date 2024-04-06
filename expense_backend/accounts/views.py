from django.db.models.functions import Trunc
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def validate_session(request):
    # Access to these fields after auth.
    return JsonResponse({
                        'isAuthenticated': True,
                        'user_permission': request.user.user_permission,
                        'user_email': request.user.email,
                        })

# These two classes are essentially "boilerplate code",
# They are responsible for creating tokens for frontend to integrate
# login functionality.
class AccountTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_permission'] = self.user.user_permission
        data['user_email'] = self.user.email
        return data

class AccountTokenObtainPairView(TokenObtainPairView):
    serializer_class = AccountTokenObtainPairSerializer


# Secure Login Method with Backend using HTTP Cookies.
class SecureLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email');
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Generate token manually.
            refresh = RefreshToken.for_user(user)

            # Set HttpOnly cookies
            response = JsonResponse({'detail' : 'Login Successful'})
            expiry = datetime.utcnow() + refresh.lifetime
            response.set_cookie(
                    'refresh_token',
                    value=str(refresh),
                    expires=expiry,
                    httponly=True, # Take away R/W access from Client side JS.
                    samesite='Strict'
            )
            response.set_cookie(
                    'access_token',
                    value=str(refresh.access_token),
                    expires=expiry,
                    httponly=True,
                    samesite='Strict'
            )

            # Other cookies here:
            response.set_cookie('user_permission', user.user_permission, httponly=True)
            response.set_cookie('user_email', user.email, httponly=True)

            return response
        return JsonResponse({'detail': 'Invalid credentials'},  status=400)


