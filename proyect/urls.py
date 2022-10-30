from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from booking.views import (
    RoomListView,
    RoomDetailView,
    EventDetailView,
    EventListView,
    BookingListView,
    RoomListView
)
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='rooms'),
    path('rooms/<int:pk>', RoomDetailView.as_view(), name='room-detail'),
    path('events/', EventListView.as_view(), name='event'),
    path('events/<int:pk>', EventDetailView.as_view(), name='event-detail'),
    path('bookings/', BookingListView.as_view(), name='booking'),
    path('bookings/<int:pk>', BookingListView.as_view(), name='booking-detail'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls), 
    path('docs/', include_docs_urls(title='Snippet API'))
]
