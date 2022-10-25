from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from booking.views import (
    UserViewSet,
    RoomViewSet,
    EventViewSet,
    BookingViewSet
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'events', EventViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
