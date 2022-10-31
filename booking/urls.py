from django.urls import path
from booking.views import (
    RoomListView,
    RoomDetailView,
    EventDetailView,
    EventListView,
    BookingListView,
)


urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='rooms'),
    path('rooms/<int:pk>', RoomDetailView.as_view(), name='room-detail'),
    path('events/', EventListView.as_view(), name='event'),
    path('events/<int:pk>', EventDetailView.as_view(), name='event-detail'),
    path('bookings/', BookingListView.as_view(), name='booking'),
    path('bookings/<int:pk>', BookingListView.as_view(), name='booking-detail'),
]
