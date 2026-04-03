import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website_sensor_licenta.settings")
django.setup()

import paho.mqtt.client as mqtt
from telemetry.models import SensorReading
from mqtt_client.topics import TELEMETRY_TOPICS


BROKER_HOST = "localhost"
BROKER_PORT = 1883
MQTT_USERNAME = None
MQTT_PASSWORD = None


def on_connect(client, userdata, flags, rc):
    print(f"MQTT connected with result code {rc}")
    for topic in TELEMETRY_TOPICS:
        client.subscribe(topic)


def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        sensor_type = topic.split("/")[-1]
        try:
            numeric_value = float(payload)
        except ValueError:
            numeric_value = None

        SensorReading.objects.create(
            sensor_type=sensor_type,
            value=numeric_value,
            unit="m" if sensor_type == "proximity" else "",
            topic=topic,
            status="normal",
            metadata={"raw_payload": payload}
        )

        print(f"Saved: {sensor_type} = {payload}")

    except Exception as e:
        print(f"Error saving message: {e}")


def start_mqtt_subscriber():
    client = mqtt.Client()

    if MQTT_USERNAME:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    start_mqtt_subscriber()


def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        sensor_type = topic.split("/")[-1]

        try:
            numeric_value = float(payload)
        except ValueError:
            numeric_value = None

        reading = SensorReading.objects.create(
            sensor_type=sensor_type,
            value=numeric_value,
            unit="m" if sensor_type == "proximity" else "",
            topic=topic,
            status="normal",
            metadata={"raw_payload": payload}
        )

        print("Saved in DB:", reading.id, reading.sensor_type, reading.value)

    except Exception as e:
        print("Error saving message:", e)