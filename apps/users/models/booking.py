from django.db import models
from django.conf import settings
from apps.users.models.vehicle import Vehicle

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user.email} - {self.vehicle.plate} ({self.start_date} to {self.end_date})"