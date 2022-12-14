from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    capacity = models.IntegerField()

class Event(models.Model):
    class Type(models.TextChoices):
        PUBLIC = 'PUB', 'Public'
        PRIVATE = 'PRI', 'Private'

    title = models.CharField(max_length=200)
    room = models.ForeignKey(
        Room,
        related_name='events', 
        on_delete=models.CASCADE, 
        unique_for_date='date'
    )
    date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(
        max_length = 3,
        choices = Type.choices,
        default = Type.PUBLIC
    )

    @property
    def spaces(self):
        return self.avialable_spaces() or None

    def avialable_spaces(self):
        return self.room.capacity - self.occupied_spaces()

    def occupied_spaces(self):
        return len(self.booking_set.all())

    def has_available_spaces(self):
        return True if self.avialable_spaces() > 0 else False

class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
