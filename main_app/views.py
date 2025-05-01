from rest_framework import viewsets, permissions, generics, serializers, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Vehicle, Reservation, Garage, Company, ParkingSpot
from .serializers import (
    VehicleSerializer,
    ReservationSerializer,
    GarageSerializer,
    CompanySerializer,
    ParkingSpotSerializer,
    UserSerializer
)

# Vehicle ViewSet
class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Reservation ViewSet
class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Company ViewSet
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # permission_classes = [IsAuthenticated]

# Garage ViewSet
class GarageViewSet(viewsets.ModelViewSet):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer
    # permission_classes = [IsAuthenticated]

# Parking Spot ViewSet
class ParkingSpotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotSerializer
    # permission_classes = [IsAuthenticated]

# ✅ Updated Registration Serializer (no passkey)
class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# Register View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    # permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        print(request)
        try:
            response = super().create(request, *args, **kwargs)
            user = User.objects.get(username=response.data['username'])
            refresh = RefreshToken.for_user(user)
            content = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': response.data
            }
            return Response(content, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
