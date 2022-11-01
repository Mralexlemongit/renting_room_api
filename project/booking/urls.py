from django.urls import path
from booking.views import (
    RoomListView,
    RoomDetailView,
    EventDetailView,
    EventListView,
    BookingListView,
    api_root,
)


urlpatterns = [
    path('', api_root),

    path('cuartos/', RoomListView.as_view(), name='room-list'),
    path('cuartos/<int:pk>', RoomDetailView.as_view(), name='room-detail'),
    path('eventos/', EventListView.as_view(), name='event-list'),
    path('eventos/<int:pk>', EventDetailView.as_view(), name='event-detail'),
    path('reservaciones/', BookingListView.as_view(), name='booking-list'),
    path('reservaciones/<int:pk>', BookingListView.as_view(), name='booking-detail'),
]
