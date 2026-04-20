import time
import random
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
PUBLISH_INTERVAL = 5  # secunde între fiecare rând de valori

TOPICS = {
    "car/sensors/proximity": "numeric",
    "car/sensors/line":      "text",
    "car/sensors/camera":    "text",
    "car/motors/status":     "text",
    "car/system/heartbeat":  "text",
}

LINE_STATES   = ["on_track", "on_track", "on_track", "left_detected", "right_detected", "lost"]
MOTOR_STATES  = ["forward", "forward", "stop", "left", "right", "reverse", "emergency"]
CAMERA_STATES = ["streaming", "streaming", "streaming", "offline", "error"]


def generate_value(topic):
    if topic == "car/sensors/proximity":
        return round(random.uniform(0.05, 2.50), 2)

    if topic == "car/sensors/line":
        return random.choice(LINE_STATES)

    if topic == "car/sensors/camera":
        return random.choice(CAMERA_STATES)

    if topic == "car/motors/status":
        return random.choice(MOTOR_STATES)

    if topic == "car/system/heartbeat":
        return "online"

    return "unknown"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[SIM] Conectat la broker {BROKER_HOST}:{BROKER_PORT}")
        print(f"[SIM] Publicare pe {len(TOPICS)} topicuri la fiecare {PUBLISH_INTERVAL}s\n")
    else:
        print(f"[SIM] Conectare esuata, cod: {rc}")


def on_disconnect(client, userdata, rc):
    print(f"[SIM] Deconectat (cod {rc})")


def main():
    client = mqtt.Client(client_id="laptop_simulator")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    print(f"[SIM] Conectare la {BROKER_HOST}:{BROKER_PORT}...")
    try:
        client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    except ConnectionRefusedError:
        print("[SIM] EROARE: Brokerul MQTT nu ruleaza!")
        print("      Porneste Mosquitto: mosquitto -v")
        return

    client.loop_start()
    time.sleep(1)  # asteapta on_connect

    cycle = 0
    while True:
        cycle += 1
        print(f"--- Ciclu #{cycle} ---")

        for topic, _ in TOPICS.items():
            value = generate_value(topic)
            client.publish(topic, str(value))
            print(f"  {topic:<35} -> {value}")

        print()
        time.sleep(PUBLISH_INTERVAL)


if __name__ == "__main__":
    main()