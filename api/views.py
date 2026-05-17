from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from telemetry.models import SensorReading
from .serializers import SensorReadingSerializer

_channel_layer = get_channel_layer()


@api_view(['GET'])
def getRoutes(request):
    routes = [{'GET': 'api/readings/'}, {'POST': 'api/broadcast/'}]
    return Response(routes)


@api_view(['GET'])
def getSensorReading(request):
    queryset = SensorReading.objects.all().order_by("-received_at")[:50]
    serializer = SensorReadingSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def broadcast_telemetry(request):
    if _channel_layer:
        async_to_sync(_channel_layer.group_send)(
            "telemetry",
            {"type": "telemetry_message", "data": request.data},
        )
    return Response({"ok": True})
