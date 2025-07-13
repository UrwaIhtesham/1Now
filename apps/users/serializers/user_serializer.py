from rest_framework import serializers
from apps.users.models import CustomUser
from apps.users.utils.validators import validate_email, validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

#class working with CustomUser
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)                           #can't be shown with API for security
    mobile_number = serializers.CharField(required=False, allow_blank=True)     #optional field

    #tells the rest framework the mode to serialize and the fields to save
    class Meta:
        model=CustomUser
        fields = ['email', 'password', 'mobile_number']

    #Input validation for email and password
    #email should be in correct format
    #password should be atleast 6 characters long and include number,letter and symbls
    def validate(self, data):
        try: 
            validate_email(data['email'])
            validate_password(data['password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"error": str(e)})
        return data 
    
    #creates and returns the user instance
    def create(self, validated_data):
        return CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            mobile_number= validated_data.get('mobile_number', '')
        )