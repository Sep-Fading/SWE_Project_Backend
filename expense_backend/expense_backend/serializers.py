from rest_framework import serializers
from accounts.models import AccountModel
from accounts.models import EmployeeFormModel

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

class JSONSerializerField(serializers.Field):
    def to_representation(self, value):
        json_data = {}
        try:
            json_data = json.loads(value)
        except ValueError as e:
            raise e
        finally:
            return json_data

    def to_internal_value(self, data):
        return json.dumps(data)

