from django.contrib import admin
from .models import Garage, ParkingSpot, Vehicle, Reservation, Company

admin.site.register(Garage)
admin.site.register(ParkingSpot)
admin.site.register(Vehicle)
admin.site.register(Reservation)
admin.site.register(Company)
