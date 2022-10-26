from dataclasses import field
from booking.models import User, Room, Event, Booking
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'role',]

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['url', 'id', 'capacity',]
    
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['url', 'title', 'room', 'date', 'type',]

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['url', 'event', 'user']