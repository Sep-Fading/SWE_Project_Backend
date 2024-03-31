from rest_framework import serializers
from accounts.models import AccountModel

# Creating serializers for our REST API 
# This lets us define models we want to fetch
# data from.
class AccountModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountModel
        fields = '__all__' # Will need to configure for future reference.

