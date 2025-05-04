from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    VehicleViewSet,
    ReservationViewSet,
    GarageViewSet,
    CompanyViewSet,
    ParkingSpotViewSet,
    RegisterView,
    LoginView,               
    GarageDetail,
    VerifyUserView
)

# Initialize router and register viewsets
# router = DefaultRouter()
# router.register(r'vehicles', VehicleViewSet, basename='vehicle')
# router.register(r'reservations', ReservationViewSet, basename='reservation')
# router.register(r'parking', ParkingSpotViewSet, basename='parking')
# router.register(r'garages', GarageViewSet, basename='garage')
# router.register(r'companies', CompanyViewSet, basename='company')

# Define URL patterns
urlpatterns = [
    path('garages/', GarageViewSet.as_view(), name='garage-index'),
    path('garages/<int:garage_id>/', GarageDetail.as_view(), name='garage-detail'),
    path('garages/<int:garage_id>/spots/', ParkingSpotViewSet.as_view(), name='garage-spots'),
    path('vehicles/users', VehicleViewSet.as_view(), name='user-vehicles'),

    # 🔐 Auth endpoints
    path('register/', RegisterView.as_view(), name='register'),   # signup
    path('users/login/', LoginView.as_view(), name='login'),      # custom login ✅

    # (Optional) JWT token endpoints if you still want them
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/', VerifyUserView.as_view(), name='token_refresh'),
]
