from rest_framework import generics
from accounts.models import AccountModel
from .serializers import AccountModelSerializer
from .serializers import EmployeeFormModelSerializer
from accounts.models import EmployeeFormModel

from django.db.models import Q
from django.shortcuts import render 
from rest_framework.views import APIView 
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from datetime import datetime

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
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get(self, request): 
        employee_forms = EmployeeFormModel.objects.all()
        serializer = EmployeeFormModelSerializer(employee_forms, many=True)
        return Response(serializer.data)


  
    def post(self, request): 
        serializer = EmployeeFormModelSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True): 
            serializer.save() 
            return  Response(serializer.data) 

class UpdateClaimStatus(APIView):
    def patch(self,request,claim_id,claim_status,approved_by,approved_on,comment):
        try:
            claim = EmployeeFormModel.objects.get(claimID=claim_id)
        except EmployeeFormModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        claim.status = claim_status
        claim.approvedBy = approved_by
        claim.dateApproved = datetime.strptime(approved_on, '%Y-%m-%d').date()
        claim.comments = comment
        claim.save()

        serializer = EmployeeFormModelSerializer(claim)
        return Response(serializer.data)

class GetClaims(APIView):
    def get(self,request,role,current_user_id,current):
        current = self.string_to_boolean(current) 
        if role == 'EMPLOYEE':
            if current:
                claims = EmployeeFormModel.objects.filter(Q(user_id = current_user_id) & (Q(status='APPROVED') | Q(status='PENDING')|Q(status='REJECTEDF')|Q(status='REJECTED')))
            else:
                claims = EmployeeFormModel.objects.filter(Q(user_id = current_user_id) & Q(status = 'PROCESSED'))

        elif role == 'LINEMANAGER':
            if current:
                claims = EmployeeFormModel.objects.filter(Q(lineManagerID = current_user_id) & (Q(status='REJECTEDF') | Q(status='PENDING')))
            else:
                claims = EmployeeFormModel.objects.filter(Q(lineManagerID = current_user_id) & (Q(status='REJECTED') | Q(status='APPROVED')|Q(status='PROCESSED')))
        else:
            if current:
                claims = EmployeeFormModel.objects.filter(status='APPROVED')
            else:
                claims = EmployeeFormModel.objects.filter(Q(status='REJECTEDF')|Q(status= 'PROCESSED'))
           
        serializer  = EmployeeFormModelSerializer(claims,many = True)
        return Response(serializer.data)

    def string_to_boolean(self,string):
        if string.lower() == 'true':
            return True
        elif string.lower() == 'false':
            return False
        else:
            raise ValueError("String is not 'true' or 'false'.")


class AcceptClaimView(APIView):
    def patch(self, request, claim_id):
        try:
            claim = EmployeeFormModel.objects.get(claimID=claim_id)
        except EmployeeFormModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        claim.status = 'APPROVED'
        claim.save()

        serializer = EmployeeFormModelSerializer(claim)
        return Response(serializer.data)
    
class RejectClaimView(APIView):
    def patch(self, request, claim_id):
        try:
            claim = EmployeeFormModel.objects.get(claimID=claim_id)
        except EmployeeFormModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        claim.status = 'REJECTED'
        claim.save()

        serializer = EmployeeFormModelSerializer(claim)
        return Response(serializer.data)

class ApprovedClaimsListView(generics.ListAPIView):
    serializer_class = EmployeeFormModelSerializer

    def get_queryset(self):
        return EmployeeFormModel.objects.filter(status='APPROVED')




@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def process_claim_status(request, claim_id):

    try:
        claim = EmployeeFormModel.objects.get(claimID=claim_id, status='APPROVED')
    except EmployeeFormModel.DoesNotExist:
        return JsonResponse({'error': 'Claim not found or not in the correct status'}, status=status.HTTP_404_NOT_FOUND)

    claim.status = 'PROCESSED'
    claim.save()

    return JsonResponse({'message': 'Claim status processed successfully'})

@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def rejectf_claim_status(request, claim_id):

    try:
        claim = EmployeeFormModel.objects.get(claimID=claim_id, status='APPROVED')
    except EmployeeFormModel.DoesNotExist:
        return JsonResponse({'error': 'Claim not found or not in the correct status'}, status=status.HTTP_404_NOT_FOUND)

    claim.status = 'REJECTEDF'
    claim.save()

    return JsonResponse({'message': 'Claim status rejected successfully'})
