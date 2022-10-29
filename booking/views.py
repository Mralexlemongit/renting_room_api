from booking.models import Booking, Room, Event
from rest_framework import viewsets
from booking.serializers import (
    BookingSerializer,
    RoomSerializer,
    EventSerializer
)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer