from django.contrib import admin
from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Booking API",
        default_version='1.0.0',
        description="""Esta api esta basada en el problema de creacion de `Eventos`, `Reservaciones` y `Habitaciones`.""",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="alexarmacode@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[]
)

urlpatterns = [
    path('',include('booking.urls')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('admin/', admin.site.urls), 
    # path('docs/', include_docs_urls(title='Booking API'))
]
