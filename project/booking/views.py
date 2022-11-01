from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from booking.models import Booking, Room, Event
from booking.permissions import IsBusinessOrReadOnly
from booking.serializers import (
    BookingListSerializer,
    RoomListSerializer,
    RoomDetailSerializer,
    EventDetailSerializer,
    EventListSerializer
)

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'cuartos': reverse('room-list', request=request, format=format),
        'eventos': reverse('event-list', request=request, format=format),
        'reservaciones': reverse('booking-list', request=request, format=format),
        'documentacion': reverse('schema-redoc', request=request, format=format),
    })

class RoomListView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer
    permission_classes = [IsBusinessOrReadOnly]

    @swagger_auto_schema(operation_description="description")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class RoomDetailView(generics.RetrieveDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer
    permission_classes = [IsBusinessOrReadOnly]

# class PublicAndOwnedEventsQuerySetMixin:
#     def get_queryset(self):
#         events = Event.objects.filter(type='PUB')
#         user = self.request.user
#         if user.groups.filter(name = 'business').exists():
#             events = events | Event.objects.filter(owner=user)
#         return events

class EventListView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    permission_classes = [IsBusinessOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class EventDetailView(generics.RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    permission_classes = [IsBusinessOrReadOnly]

class BookingListView(generics.ListCreateAPIView):
    serializer_class = BookingListSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    @swagger_auto_schema(operation_description="description")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            booking = Booking.objects.filter(user=self.request.user)
            return booking | self.booking_from_business()

        return Booking.objects.none()
    
    def booking_from_business(self):
        booking = Booking.objects.none()
        if self.request.user.groups.filter(name = 'business').exists():
            user_events = Event.objects.filter(owner=self.request.user)
            for event in user_events:
                booking |= event.booking_set.all()
        return booking

    def perform_create(self, serializer):
        pk = self.request.POST.get('user')
        if pk:
            user = User.objects.get(pk=pk)
            serializer.save(user=user)
        else:
            serializer.save(user=self.request.user)