from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from booking.views import (
    RoomListView,
    RoomDetailView,
    EventViewSet,
    EventListView,
    BookingViewSet,
    RoomListView
)
from rest_framework.documentation import include_docs_urls

router = routers.DefaultRouter()
router.register(r'eventss', EventViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='rooms'),
    path('rooms/<int:pk>', RoomDetailView.as_view(), name='room-detail'),
    path('events/', EventListView.as_view(), name='event'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls), 
    path('docs/', include_docs_urls(title='Snippet API'))
]
