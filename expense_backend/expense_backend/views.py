from rest_framework import generics
from accounts.models import AccountModel
from .serializers import AccountModelSerializer

# Here we are creating a view that can handle
# API requests and return data in JSON format.
# For this we use DRF's Generic Views.
class AccountModelListCreate(generics.ListCreateAPIView):
    queryset = AccountModel.objects.all()
    serializer_class = AccountModelSerializer



