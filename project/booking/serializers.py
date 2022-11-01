from booking.models import Room, Event, Booking
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueForDateValidator

# User Serializer:
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'group']

# Hiperlink serializers

class RoomHyperlinkedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'url']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["numero_cuarto"] = rep["id"]
        rep.pop("id", None)
        rep['url'] = rep.pop("url")
        return rep

# Regular serializers

event_unic_for_date_validation = UniqueForDateValidator(
    queryset = Event.objects.all(),
    field = 'room',
    date_field = 'date',
    message = "Cannot create event in room with day reserved."
)

class EventListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.first_name')
    room = RoomHyperlinkedSerializer()

    class Meta:
        model = Event
        fields = ['url', 'title', 'room', 'date', 'type', 'owner']
        validators = [
            event_unic_for_date_validation
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["titulo"] = rep["title"]
        rep.pop("title", None)
        rep["tipo"] = dict(Event.Type.choices)[rep["type"]]
        rep.pop("type", None)
        rep["fecha"] = rep["date"]
        rep.pop("date", None)
        rep["organizador"] = rep["owner"]
        rep.pop("owner", None)
        rep["cuarto"] = rep["room"]
        rep.pop("room", None)

        return rep


class EventDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.first_name')

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
        rep['user'] = User.objects.get(pk=rep['user']).first_name
        return rep

    def validate_event(self, event):
        if not event.has_available_spaces():
            raise serializers.ValidationError("Event has no spaces available.")
        return event

class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'capacity', 'url',]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["numero_cuarto"] = rep["id"]
        rep.pop("id", None)
        rep["capacidad"] = rep["capacity"]
        rep.pop("capacity", None)
        return rep

class RoomDetailSerializer(serializers.ModelSerializer):
    events = EventListSerializer(
        many = True,
        read_only = True,
    )

    class Meta:
        model = Room
        fields = ['id', 'capacity', 'events', ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["numero_cuarto"] = rep["id"]
        rep.pop("id", None)
        rep["capacidad"] = rep["capacity"]
        rep.pop("capacity", None)
        rep["eventos"] = rep["events"]
        rep.pop("events", None)
        return rep
