from django.urls import path
from .views import getRoutes, getSensorReading, broadcast_telemetry

urlpatterns = [
    path("", getRoutes, name="api-routes"),
    path("readings/", getSensorReading, name="sensor-readings"),
    path("broadcast/", broadcast_telemetry, name="broadcast-telemetry"),
]