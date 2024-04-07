from weakref import ref
from rest_framework.response import Response 
from rest_framework import status
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authentication import get_authorization_header


# This takes care of serialization of our data from
# AccountModel. Which is then used by the AccountTokenObtainPairView
# to create a JSON response to be sent to the front end.
class AccountTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # For redirecting to the right page after login.
        user_permission = self.user.user_permission
        redirect_url = self.get_redirect_url(user_permission);
        # Adding our custom data in the response.
        data.update({
                    'user_permission': self.user.user_permission,
                    'user_email': self.user.email,
                    'redirect_url': redirect_url,
        })
        return data
    
    def get_redirect_url(self, permission):
        redirect_urls = {
                'EMPLOYEE': settings.FRONTEND_URL + '/new_claim',
                'FINANCE': settings.FRONTEND_URL + '/Finance',
                'LINEMANAGER': settings.FRONTEND_URL + '/LineManager',
                'ADMIN': settings.FRONTEND_URL + '/admin',
        }

        return redirect_urls.get(permission, settings.FRONTEND_URL + '/Login')


class AccountTokenObtainPairView(TokenObtainPairView):
    serializer_class = AccountTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.user
        tokens = get_tokens_for_user(user)

        # Get redirect_url from serilizer's validated data.
        redirect_url = serializer.validated_data.get('redirect_url')

        # Prepare the response with tokens and user info.
        response_data = {
                'access_token' : tokens['access'],
                'refresh_token': tokens['refresh'],
                'user_permission': user.user_permission,
                'user_email': user.email,
                'redirect_url': redirect_url,
        }

        # Making HttpOnly cookies for tokens instead of sending them 
        # in the body.
        response = Response(response_data, status=status.HTTP_200_OK)
        set_token_cookies(response, tokens)
        return response


# Gets the token for a user.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
    }

# Set tokens as HTTP Cookies with defined lifetimes.
def set_token_cookies(response, tokens):
    max_age = 3600 # 1 hour for access token
    refresh_max_age = 3600*24*30 # 30 days for refresh token

    response.set_cookie(
            key='access_token',
            value=tokens['access'],
            httponly=True,
            samesite='Lax',
            secure=settings.SECURE_SSL_REDIRECT,
            max_age=max_age
    )

    response.set_cookie(
            key='refresh_token',
            value=tokens['refresh'],
            httponly=True,
            samesite='Lax',
            secure=settings.SECURE_SSL_REDIRECT,
            max_age=refresh_max_age
    )

# Session Validation Function - Used by frontend to 
# ensure authorized page access.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def validate_session(request):
    
    # Auth header (use for debugging:
    """
    auth_header = get_authorization_header(request).decode('utf-8')
    print(request.headers)
    print(auth_header)
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split('Bearer ')[1]
        print("Received token: ", token)
    else:
        print("No valid Auth header found!")
    """

    user_permission = request.user.user_permission
    return JsonResponse({
                        'isAuthenticated': True,
                        'userPermission': user_permission,
    })
