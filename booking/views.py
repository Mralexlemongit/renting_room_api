from asyncio import events
from rest_framework import mixins
from booking.models import Booking, Room, Event
from booking.permissions import IsBusinessOrReadOnly
from rest_framework import generics, viewsets
from booking.serializers import (
    BookingSerializer,
    RoomListSerializer,
    RoomDetailSerializer,
    EventSerializer,
    EventListSerializer
)

class RoomListView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer
    permission_classes = [IsBusinessOrReadOnly]

class RoomDetailView(generics.RetrieveDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer
    permission_classes = [IsBusinessOrReadOnly]

class EventListView(generics.ListCreateAPIView):
    serializer_class = EventListSerializer
    permission_classes = [IsBusinessOrReadOnly]

    def get_queryset(self):
        events = Event.objects.filter(type='PUB')
        user = self.request.user
        if user.groups.filter(name = 'business').exists():
            events = events | Event.objects.filter(owner=user)
        return events

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer