from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from booking.views import (
    RoomViewSet,
    EventViewSet,
    BookingViewSet
)
from rest_framework.documentation import include_docs_urls

router = routers.DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'events', EventViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls), 
    path('docs/', include_docs_urls(title='Snippet API'))
]
