from django.shortcuts import render
from telemetry.models import SensorReading


def home(request):
    recent_readings = SensorReading.objects.order_by('-created_at')[:10]

    latest_readings = {}
    for reading in SensorReading.objects.order_by('-created_at'):
        if reading.sensor_type not in latest_readings:
            latest_readings[reading.sensor_type] = reading

    context = {
        'latest_readings': latest_readings.values(),
        'recent_readings': recent_readings,
    }

    return render(request, 'dashboard/home.html', context)