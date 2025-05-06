from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import *

# Define URL patterns
urlpatterns = [
    path('garages/', GarageViewSet.as_view(), name='garage-index'),
    path('garages/<int:garage_id>/', GarageDetail.as_view(), name='garage-detail'),
    path('garages/<int:garage_id>/spots/', ParkingSpotViewSet.as_view(), name='garage-spots'),
    path('vehicles/', VehicleApiView.as_view(), name='user-vehicles'),
    path('users/register/', CreateUserView.as_view(), name='register'),   # signup
    path('users/login/', LoginView.as_view(), name='login'),      # custom login ✅

    # (Optional) JWT token endpoints if you still want them
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/', VerifyUserView.as_view(), name='token_refresh'),
    path('reservations/<int:pk>/', ReservationAPIView.as_view(), name='reservation-delete'),
    path('reservations/', ReservationAPIView.as_view(), name='reservation-list-create'),

]
