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

#This is the serializer for the UserInfo model.
class UserInfoModelSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField()
    class Meta:
        model = UserInfoModel
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'zip_code', 'city', 'country', 'account_number', 'sort_code', 'tax_code', 'manager_id', 'role']


# Serializers for update details on admin side.
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfoModel;
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'tax_code']

# Serializers for update details on admin side.
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfoModel;
        fields = ['address', 'zip_code', 'city', 'country']

# Serializers for update details on admin side.
class BankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfoModel;
        fields = ['account_number', 'sort_code']

