from django.urls import path
from .views import SensorReadingListView

urlpatterns = [
    path("readings/", SensorReadingListView.as_view(), name="sensor-readings"),
]