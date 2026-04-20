from rest_framework import generics
from telemetry.models import SensorReading
from .serializers import SensorReadingSerializer


class SensorReadingListView(generics.ListAPIView):
    queryset = SensorReading.objects.all().order_by("-received_at")[:50]  # <-- schimbat
    serializer_class = SensorReadingSerializer