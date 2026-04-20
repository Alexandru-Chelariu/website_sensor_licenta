from rest_framework import serializers
from telemetry.models import SensorReading, MachineSystem, Sensor, SensorCategory


class SensorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorCategory
        fields = ["id", "name", "label"]


class SensorSerializer(serializers.ModelSerializer):
    category = SensorCategorySerializer(read_only=True)

    class Meta:
        model = Sensor
        fields = ["id", "sensor_id", "label", "unit", "is_numeric", "category"]


class MachineSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineSystem
        fields = ["id", "system_uid", "machine_type", "machine_id", "label", "last_seen"]


class SensorReadingSerializer(serializers.ModelSerializer):
    system  = MachineSystemSerializer(read_only=True)
    sensor  = SensorSerializer(read_only=True)

    class Meta:
        model = SensorReading
        fields = [
            "id",
            "system",
            "sensor",
            "raw_value",
            "numeric_value",
            "unit",
            "status",
            "topic",
            "received_at",   # <-- numele corect
        ]