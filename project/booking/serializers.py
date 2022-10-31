from booking.models import Room, Event, Booking
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueForDateValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'group']

event_unic_for_date_validation = UniqueForDateValidator(
    queryset = Event.objects.all(),
    field = 'room',
    date_field = 'date',
    message = "Cannot create event in room with day reserved."
)

class EventListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Event
        fields = ['url', 'title', 'room', 'date', 'type', 'owner']
        validators = [
            event_unic_for_date_validation
        ]

class EventDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Event
        fields = ['title', 'room', 'date', 'type', 'owner']
        validators = [
            event_unic_for_date_validation
        ]

class BookingListSerializer(serializers.ModelSerializer):
    user =  serializers.PrimaryKeyRelatedField(
        read_only=True, 
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Booking
        fields = ['url', 'event', 'user', ]
        validators = [
            UniqueTogetherValidator(
                queryset=Booking.objects.all(),
                fields=['event', 'user'],
                message= "Cannot book twice one event."
            )
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['event'] = Event.objects.get(pk=rep['event']).title
        rep['user'] = User.objects.get(pk=rep['user']).username
        return rep

    def validate_event(self, event):
        if not event.has_available_spaces():
            raise serializers.ValidationError("Event has no spaces available.")
        return event

class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['url', 'id', 'capacity',]

class RoomDetailSerializer(serializers.ModelSerializer):
    events = EventListSerializer(
        many = True,
        read_only = True,
    )

    class Meta:
        model = Room
        fields = ['id', 'capacity', 'events', ]
