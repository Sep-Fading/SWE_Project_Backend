from rest_framework import generics
from accounts.models import AccountModel
from .serializers import AccountModelSerializer
from .serializers import EmployeeFormModelSerializer
from accounts.models import EmployeeFormModel

from django.shortcuts import render 
from rest_framework.views import APIView 
from rest_framework.response import Response

# Here we are creating a view that can handle
# API requests and return data in JSON format.
# For this we use DRF's Generic Views.
class AccountModelListCreate(generics.ListCreateAPIView):
    queryset = AccountModel.objects.all()
    serializer_class = AccountModelSerializer

# Create your views here.

#View for Employee Form claim
class EmployeeFormView(APIView): 
    
    serializer_class = EmployeeFormModelSerializer 
  
    def get(self, request): 
        detail = [ {"amount": detail.amount,"currency": detail.currency, "typeClaim": detail.typeClaim,"description": detail.description, "acknowledgement": detail.acknowledgement}  
        for detail in EmployeeFormModel.objects.all()] 
        return Response(detail) 
  
    def post(self, request): 
  
        serializer = EmployeeFormModelSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True): 
            serializer.save() 
            return  Response(serializer.data) 

