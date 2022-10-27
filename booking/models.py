from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Type(models.TextChoices):
        BUSINESS = 'BUS', 'Bussines'
        CUSTOMER = 'CUS', 'Customer'

    role = models.CharField(
        max_length = 3,
        choices = Type.choices,
        default = Type.CUSTOMER
    )

class Room(models.Model):
    capacity = models.IntegerField()

class Event(models.Model):
    class Type(models.TextChoices):
        PUBLIC = 'PUB', 'Public'
        PRIVATE = 'PRI', 'Private'

    title = models.CharField(max_length=200)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, unique_for_date='date')
    date = models.DateField()
    type = models.CharField(
        max_length = 3,
        choices = Type.choices,
        default = Type.PUBLIC
    )

    def occupied_spaces(self):
        return len(self.booking_set.all())

    def has_available_spaces(self):
        return True if self.room.capacity > self.occupied_spaces() else False

class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
