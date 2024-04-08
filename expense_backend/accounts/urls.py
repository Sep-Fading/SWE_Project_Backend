from django.urls import path
from .views import AccountTokenObtainPairView
from .views import validate_session
from .views import UserInfoListView
from .views import logout_view
from .views import UserInfoSpecificView
from .views import UpdateUserInfo

urlpatterns = [
        path('api/token/', AccountTokenObtainPairView.as_view(),
             name='token_obtain_pair'),
        path('api/validate_session/', validate_session, name='validate_session'),
        path('api/user-info/', UserInfoListView.as_view(), name='user-info-list'),
        path('api/user-info/<int:uid>/', UserInfoSpecificView.as_view(), name='user-info-specific'),
        path('api/user-info/update/<int:uid>/', UpdateUserInfo.as_view(), name='update_user_info'),
        path('api/logout/', logout_view, name='logout'),
]
