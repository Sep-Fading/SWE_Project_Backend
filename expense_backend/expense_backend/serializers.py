from rest_framework import serializers
from accounts.models import AccountModel
from accounts.models import EmployeeFormModel
from accounts.models import UserInfoModel

# Creating serializers for our REST API 
# This lets us define models we want to fetch
# data from.
class AccountModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountModel
        fields = '__all__' # Will need to configure for future reference.

#This is the serializer for the employee claims form
class EmployeeFormModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeFormModel
        fields = '__all__' 

#This is the serializer for the employee claims form
class UserInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfoModel
        fields = '__all__' 



