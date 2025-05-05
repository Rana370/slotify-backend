from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=100)
    passkey = models.CharField(max_length=100)
    employees = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company', null=True)

    def __str__(self):
        return self.name

class Garage(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='garages', null=True)

    def __str__(self):
        return self.name

class ParkingSpot(models.Model):
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, related_name='spots')
    number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Spot {self.number} in {self.garage.name}"

class Vehicle(models.Model):
    plate_number = models.CharField(max_length=20)
    model = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default="#000000")  # ✅ New color field
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.plate_number





class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE)
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, related_name='reservations', null=True)  # ✅ New field
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.parking_spot.number}"
