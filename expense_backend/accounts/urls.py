from django.urls import path
from .views import AccountTokenObtainPairView
from .views import validate_session

urlpatterns = [
        path('api/token/', AccountTokenObtainPairView.as_view(),
             name='token_obtain_pair'),
        path('api/validate_session', validate_session, name='validate_session'),
]
