import os, sys
from pathlib import Path
from datetime import datetime

import django
import paho.mqtt.client as mqtt
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website_sensor_licenta.settings")
django.setup()

from telemetry.models import MachineSystem, SensorCategory, Sensor, SensorReading
from mqtt_client.topics import SENSORS

BROKER_HOST = "localhost"
BROKER_PORT = 1883
SUBSCRIBE_WILDCARD = "+/+/+/+"  # machine_type/machine_id/category/sensor_id

channel_layer = get_channel_layer()


def get_status(sensor_id, category, numeric_value, raw_value):
    if category == "engine":
        if sensor_id == "temperature" and numeric_value and numeric_value > 105:
            return "critical"
        if sensor_id == "oil_pressure" and numeric_value and numeric_value < 1.5:
            return "critical"
        if sensor_id == "status" and raw_value == "fault":
            return "fault"

    if category == "accident_prevention":
        if "distance" in sensor_id and numeric_value and numeric_value < 0.5:
            return "critical"
        if "distance" in sensor_id and numeric_value and numeric_value < 1.5:
            return "warning"
        if sensor_id == "alarm" and raw_value != "none":
            return "critical"

    if category == "hydraulic":
        if "pressure" in sensor_id and numeric_value and numeric_value > 250:
            return "critical"
        if sensor_id == "oil_temperature" and numeric_value and numeric_value > 85:
            return "warning"

    if category == "pneumatic":
        if "pressure" in sensor_id and numeric_value and numeric_value < 4:
            return "critical"
        if sensor_id == "brake_status" and raw_value == "fault":
            return "fault"

    if category == "environment":
        if sensor_id == "gas_co" and numeric_value and numeric_value > 50:
            return "critical"
        if sensor_id == "air_quality" and numeric_value and numeric_value > 150:
            return "warning"

    if raw_value in ["fault", "error", "offline", "lost"]:
        return "fault"

    return "normal"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[MQTT] Conectat la {BROKER_HOST}:{BROKER_PORT}")
        client.subscribe(SUBSCRIBE_WILDCARD)
        print(f"[MQTT] Subscribing la: {SUBSCRIBE_WILDCARD}")
    else:
        print(f"[MQTT] Eroare conectare: rc={rc}")


def on_message(client, userdata, msg):
    try:
        parts = msg.topic.split("/")
        if len(parts) != 4:
            return  # ignoram topicuri care nu respecta formatul

        machine_type, machine_id, category_name, sensor_id = parts
        raw_value = msg.payload.decode("utf-8").strip()

        # Gaseste sau creaza MachineSystem
        system, _ = MachineSystem.objects.get_or_create(
            machine_id=machine_id,
            defaults={
                "system_uid": f"{machine_type}-{machine_id}",
                "machine_type": machine_type,
                "label": f"{machine_type.capitalize()} {machine_id}",
            }
        )
        system.last_seen = datetime.now()
        system.save(update_fields=["last_seen"])

        # Gaseste sau creaza SensorCategory
        category, _ = SensorCategory.objects.get_or_create(
            name=category_name,
            defaults={"label": category_name.replace("_", " ").title()}
        )

        # Gaseste sau creaza Sensor
        meta = SENSORS.get(category_name, {}).get(sensor_id, {})
        sensor, _ = Sensor.objects.get_or_create(
            category=category,
            sensor_id=sensor_id,
            defaults={
                "label":       meta.get("desc", sensor_id),
                "unit":        meta.get("unit", ""),
                "is_numeric":  meta.get("numeric", True),
                "description": meta.get("desc", ""),
            }
        )

        # Valoare numerica
        numeric_value = None
        if sensor.is_numeric:
            try:
                numeric_value = float(raw_value)
            except ValueError:
                pass

        status = get_status(sensor_id, category_name, numeric_value, raw_value)

        # Salveaza reading
        reading = SensorReading.objects.create(
            system=system,
            sensor=sensor,
            raw_value=raw_value,
            numeric_value=numeric_value,
            unit=sensor.unit,
            status=status,
            topic=msg.topic,
        )

        # Trimite live in dashboard
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                "telemetry",
                {
                    "type": "telemetry_message",
                    "data": {
                        "id":             reading.id,
                        "machine_type":   system.machine_type,
                        "machine_id":     system.machine_id,
                        "category":       category_name,
                        "sensor_id":      sensor_id,
                        "raw_value":      raw_value,
                        "numeric_value":  numeric_value,
                        "unit":           sensor.unit,
                        "status":         status,
                        "topic":          msg.topic,
                        "received_at":    reading.received_at.isoformat(),
                    }
                }
            )

        print(
            f"[{system.machine_id}] {category_name}/{sensor_id} = "
            f"{raw_value} {sensor.unit} [{status}]"
        )

    except Exception as e:
        print(f"[MQTT] Eroare procesare mesaj: {e}")


def start_mqtt_subscriber():
    client = mqtt.Client(client_id="django_subscriber")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_forever()


if __name__ == "__main__":
    start_mqtt_subscriber()