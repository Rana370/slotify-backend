from rest_framework import serializers
from .models import Vehicle, Reservation, Garage, ParkingSpot, Company
from django.contrib.auth.models import User

# --------------------------
# User Serializer
# --------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

# --------------------------
# Company Serializer
# --------------------------
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

# --------------------------
# Garage Serializer
# --------------------------
class GarageSerializer(serializers.ModelSerializer):
    available_spots = serializers.SerializerMethodField()
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True
    )

    class Meta:
        model = Garage
        fields = ['id', 'name', 'location', 'company', 'company_id', 'available_spots']

    def get_available_spots(self, obj):
        return ParkingSpot.objects.filter(garage=obj.id, is_available=True).count()

# --------------------------
# Parking Spot Serializer with 'is_reserved'
# --------------------------
class ParkingSpotSerializer(serializers.ModelSerializer):
    garage = GarageSerializer(read_only=True)
    is_reserved = serializers.SerializerMethodField()

    class Meta:
        model = ParkingSpot
        fields = ['id', 'garage', 'number', 'is_available', 'is_reserved']

    def get_is_reserved(self, obj):
        return Reservation.objects.filter(parking_spot=obj).exists()

# --------------------------
# Vehicle Serializer with 'type' support
# --------------------------
class VehicleSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'plate_number', 'model', 'type', 'color', 'user']

# --------------------------
# Reservation Serializer
# --------------------------
class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
