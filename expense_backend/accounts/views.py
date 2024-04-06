from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response



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
