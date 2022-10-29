from rest_framework import mixins
from booking.models import Booking, Room, Event
from booking.permissions import IsBusinessOrReadOnly
from rest_framework import generics, viewsets
from booking.serializers import (
    BookingSerializer,
    RoomListSerializer,
    RoomDetailSerializer,
    EventSerializer
)

class RoomListView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer
    permission_classes = [IsBusinessOrReadOnly]

class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer