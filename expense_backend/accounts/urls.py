from django.urls import path
from .views import AccountTokenObtainPairView


urlpatterns = [
        path('api/token/', AccountTokenObtainPairView.as_view(),
             name='token_obtain_pair'),
]
