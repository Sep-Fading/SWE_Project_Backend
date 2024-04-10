"""
URL configuration for expense_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import AccountModelListCreate
from .views import EmployeeFormView
from .views import AcceptClaimView
from .views import RejectClaimView
from .views import ApprovedClaimsListView
from.views import UpdateClaimStatus
from.views import GetClaims
from .views import process_claim_status, rejectf_claim_status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accountmodel/', AccountModelListCreate.as_view(),
         name='accountmodel-list-create'),
    path('accounts/', include('accounts.urls')),
     path('api/employeeformmodel/', EmployeeFormView.as_view(),name='employee-form-view'),
    path('claims/<int:claim_id>/accept/', AcceptClaimView.as_view(), name='accept-claim'),
    path('claims/<int:claim_id>/reject/', RejectClaimView.as_view(), name='reject-claim'),
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
       path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
       path('api/approved/', ApprovedClaimsListView.as_view(),name='approved-form-view'),
    path('process_claim/<int:claim_id>/', process_claim_status, name='process_claim'),
    path('rejectf_claim/<int:claim_id>/', rejectf_claim_status, name='rejectf_claim'),
    path('update-claim-status/<int:claim_id>/<str:claim_status>/<str:approved_by>/<str:approved_on>/<str:comment>/', UpdateClaimStatus.as_view(), name='update_claim_status'),
    path('get-claims/<str:role>/<str:current>/<int:current_user_id>/',GetClaims.as_view(),name='get-claims')
]

