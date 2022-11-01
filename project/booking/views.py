from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
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

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def booking_event(request, pk, format=None):
    data = {"user": request.user.id, "event": pk}
    serializer = BookingListSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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