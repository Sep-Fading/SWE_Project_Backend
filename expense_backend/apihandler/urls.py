from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet

# DRF To auto generate some url patterns for AccountViewSet.
router = DefaultRouter()
router.register(r'accounts', AccountViewSet)

# URL Patterns
urlpatterns = [
        path('', include(router.urls)),
]




