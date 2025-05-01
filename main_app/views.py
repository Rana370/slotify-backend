from rest_framework import viewsets, permissions, generics, serializers, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ModelSerializer
from .models import Vehicle, Reservation, Garage, Company, ParkingSpot
from .serializers import (
    VehicleSerializer,
    ReservationSerializer,
    GarageSerializer,
    CompanySerializer,
    ParkingSpotSerializer
)


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)

    def perform_create(self, serializer, request):
        # serializer=self.serializer_class(user=self.request.user)
        serializer=self.serializer_class(user=User.objects.filter(user=1))
        print("user", request.user)
        print("request", request)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            



class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class GarageViewSet(viewsets.ModelViewSet):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer


class ParkingSpotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotSerializer


class RegisterSerializer(ModelSerializer):
    passkey = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'passkey']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_passkey(self, value):
        if value != '1234':
            raise serializers.ValidationError("Invalid passkey.")
        return value

    def create(self, validated_data):
        validated_data.pop('passkey')  # Remove passkey before creating user
        return User.objects.create_user(**validated_data)


# ✅ Register view
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
