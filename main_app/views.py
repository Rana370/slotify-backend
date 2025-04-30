from rest_framework import viewsets, permissions
from .models import Vehicle, Reservation, Garage, Company, ParkingSpot
from .serializers import VehicleSerializer, ReservationSerializer, GarageSerializer, CompanySerializer, ParkingSpotSerializer
from django.contrib.auth.models import User

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]


class GarageViewSet(viewsets.ModelViewSet):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer
    # permission_classes = [permissions.IsAuthenticated]

class ParkingSpotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSpot.objects.all()
    serializer_class =ParkingSpotSerializer
    permission_classes = [permissions.IsAuthenticated]
