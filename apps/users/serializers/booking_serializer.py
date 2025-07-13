from rest_framework import serializers
from apps.users.models.booking import Booking
from apps.users.utils.validators import validate_dates, validate_overlap
from django.core.exceptions import ValidationError as DjangoValidationError

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'vehicle', 'start_date', 'end_date']

    def validate(self, data):
        try:
            validate_dates(data['start_date'], data['end_date'])
            validate_overlap(data['vehicle'], data['start_date'], data['end_date'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"error": str(e)})
        
        return data