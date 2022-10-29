from asyncio import events
from booking.models import Room, Event, Booking
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueForDateValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'group']

class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['url', 'id', 'capacity',]

class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'capacity',]

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['url', 'title', 'room', 'date', 'type',]
        validators = [
            UniqueForDateValidator(
                queryset = Event.objects.all(),
                field = 'room',
                date_field = 'date',
                message = "Cannot create event in room with day reserved."
            )
        ]

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['url', 'title', 'room', 'date', 'type',]
        validators = [
            UniqueForDateValidator(
                queryset = Event.objects.all(),
                field = 'room',
                date_field = 'date',
                message = "Cannot create event in room with day reserved."
            )
        ]

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['url', 'event', 'user']
        validators = [
            UniqueTogetherValidator(
                queryset=Booking.objects.all(),
                fields=['event', 'user'],
                message= "Cannot book twice one event."
            )
        ]

    def validate_event(self, event):
      if event.has_available_spaces():
          return event
      raise serializers.ValidationError("Event has no spaces available.")