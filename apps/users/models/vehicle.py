from django.db import models
from django.conf import settings

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)             #id for the vehicle
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=100)             #Char field for make of the car
    model = models.CharField(max_length=100)            #char field for model of the car
    year = models.IntegerField()                        #integer field for year of the car
    plate=models.CharField(max_length=20, unique=True)  #license plate of the car

    def __str__(self):
        return f"{self.make} {self.model} {self.year} {self.plate}"
