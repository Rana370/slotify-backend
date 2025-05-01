from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    VehicleViewSet,
    ReservationViewSet,
    GarageViewSet,
    CompanyViewSet,
    ParkingSpotViewSet,
    RegisterView,
)

# Initialize router and register viewsets
router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'parking', ParkingSpotViewSet, basename='parking')
router.register(r'garages', GarageViewSet, basename='garage')
router.register(r'companies', CompanyViewSet, basename='company')

# Define URL patterns
urlpatterns = [
    path('', include(router.urls)),

    # JWT Auth endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Custom register route
    path('register/', RegisterView.as_view(), name='register'),
]
