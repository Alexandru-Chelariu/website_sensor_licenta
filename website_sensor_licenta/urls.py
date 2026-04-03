from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('dashboard.urls')),
    path('api/', include('api.urls')),
    path('devices/', include('devices.urls')),
    path('telemetry/', include('telemetry.urls')),
    path('alerts/', include('alerts.urls')),
    path('control/', include('control.urls')),
    path('analytics/', include('analytics.urls')),
]