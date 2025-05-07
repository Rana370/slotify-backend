from rest_framework import viewsets, permissions, generics, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404


from .models import Vehicle, Reservation, Garage, Company, ParkingSpot
from .serializers import (
    VehicleSerializer,
    ReservationSerializer,
    GarageSerializer,
    CompanySerializer,
    ParkingSpotSerializer,
    UserSerializer
)

# --------------------------
# ✅ Login View
# --------------------------
class LoginView(APIView):
    # permission_classes = [AllowAny]

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                content = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }
                return Response(content, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    try:
      user = User.objects.get(username=request.user.username)
      try:
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh),'access': str(refresh.access_token),'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
      except Exception as token_error:
        return Response({"detail": "Failed to generate token.", "error": str(token_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as err:
      return Response({"detail": "Unexpected error occurred.", "error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --------------------------
# ✅ Register View & Serializer
# --------------------------
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            user = User.objects.get(username=response.data['username'])
            refresh = RefreshToken.for_user(user)
            content = {'refresh': str(refresh), 'access': str(refresh.access_token), 'user': response.data }
            return Response(content, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response({ 'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --------------------------
# ✅ Vehicle ViewSet (with type support)
# --------------------------

# class VehicleApiView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         vehicles = Vehicle.objects.filter(user=request.user)
#         serializer = VehicleSerializer(vehicles, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = VehicleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

class VehicleListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vehicles = Vehicle.objects.filter(user=request.user)
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class VehicleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk, user=request.user)
        serializer = VehicleSerializer(vehicle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk, user=request.user)
        vehicle.delete()
        return Response(status=204)


# --------------------------
# ✅ Reservation ViewSet
# --------------------------
class ReservationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reservations = Reservation.objects.filter(user=request.user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
        serializer = ReservationSerializer(reservation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
        reservation.delete()
        return Response({"message": "Reservation deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    # create delete function in view

# --------------------------
# ✅ Company ViewSet
# --------------------------
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

# --------------------------
# ✅ Garage ViewSet
# --------------------------
class GarageViewSet(APIView):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # print("this should be going off")
            garages = Garage.objects.all()
            data = GarageSerializer(garages, many=True)
            # print(data, "checking garages")
            return Response(data.data, status=status.HTTP_200_OK)
        except Exception as err:
            # print(str(err), "checking er")
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GarageDetail(APIView):
    serializer_class = GarageSerializer

    def get(self, request, garage_id):
        try:
            garage = Garage.objects.get(id=garage_id)
            serializer = GarageSerializer(garage)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Garage.DoesNotExist:
            return Response({'error': 'Garage not found'}, status=status.HTTP_404_NOT_FOUND)

# --------------------------
# ✅ Parking Spot ViewSet
# --------------------------
class ParkingSpotViewSet(APIView):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, garage_id):
        try:
            spots = ParkingSpot.objects.filter(garage=garage_id)
            serializer = ParkingSpotSerializer(spots, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Garage.DoesNotExist:
            return Response({'error': 'Garage not found'}, status=status.HTTP_404_NOT_FOUND)



