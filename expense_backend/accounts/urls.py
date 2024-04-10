from django.urls import path
from .views import AccountTokenObtainPairView
from .views import validate_session
from .views import UserInfoListView
from .views import LogoutAPIView
from .views import UserInfoSpecificView
from .views import UpdateUserInfo
from .views import FlagPasswordChange
from .views import ChangePassword

urlpatterns = [
        path('api/token/', AccountTokenObtainPairView.as_view(),
             name='token_obtain_pair'),
        path('api/validate_session/', validate_session, name='validate_session'),
        path('api/user-info/', UserInfoListView.as_view(), name='user-info-list'),
        path('api/user-info/<int:uid>/', UserInfoSpecificView.as_view(), name='user-info-specific'),
        path('api/user-info/update/<int:uid>/', UpdateUserInfo.as_view(), name='update_user_info'),
        path('api/user-info/flag-password/<int:uid>/', FlagPasswordChange.as_view(), name='flagged-pw'),
        path('api/changepassword/', ChangePassword.as_view(), name='change-pw'),
        path('api/logout/', LogoutAPIView.as_view() , name='logout'),
]
