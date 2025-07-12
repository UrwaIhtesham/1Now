from rest_framework import serializers
from apps.users.models.vehicle import Vehicle
from apps.users.utils.validators import validate_make, validate_plate
from django.core.exceptions import ValidationError as DjangoValidationError

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'make', 'model', 'year', 'plate']

    def validate(self, data):
        try:
            validate_make(data['make'])
            validate_plate(data['plate'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"error": str(e)})
        
        return data