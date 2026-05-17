"""
Simulator MQTT pentru utilaje de constructii.
Publica date realiste pe topicuri: {machine_type}/{machine_id}/{category}/{sensor_id}
"""
import time
import random
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
PUBLISH_INTERVAL = 20 # secunde intre cicluri

MACHINES = [
    {
        "machine_type": "bulldozer",
        "machine_id": "BD-001",
        "gps_base": (44.4268, 26.1025),
        "sensors": {
            "engine":              ["rpm", "temperature", "oil_pressure", "load",
                                    "fuel_level", "coolant_temp", "status"],
            "hydraulic":           ["pressure_main", "pressure_tool", "pressure_lift",
                                    "oil_temperature", "oil_level"],
            "transmission":        ["left_speed", "right_speed", "left_tension",
                                    "right_tension", "drive_mode", "drive_status"],
            "tool":                ["angle_pitch", "angle_tilt", "height", "load", "position"],
            "accident_prevention": ["front_distance", "rear_distance", "pitch",
                                    "roll", "alarm", "seatbelt"],
            "environment":         ["temperature", "humidity", "gas_co", "noise_level"],
            "gps":                 ["latitude", "longitude", "speed", "heading", "satellites"],
            "system":              ["heartbeat", "uptime", "signal_strength"],
        },
    },
    # {
    #     "machine_type": "excavator",
    #     "machine_id": "EX-001",
    #     "gps_base": (44.4285, 26.1040),
    #     "sensors": {
    #         "engine":              ["rpm", "temperature", "oil_pressure", "load",
    #                                 "fuel_level", "status"],
    #         "hydraulic":           ["pressure_c1", "pressure_c2", "pressure_c3", "pressure_c4",
    #                                 "oil_temperature", "oil_level", "flow_rate"],
    #         "tool":                ["angle_pitch", "rotation", "reach", "open_angle",
    #                                 "load", "status"],
    #         "accident_prevention": ["front_distance", "rear_distance", "pitch", "roll", "alarm"],
    #         "environment":         ["temperature", "gas_co", "noise_level", "dust_pm10"],
    #         "gps":                 ["latitude", "longitude", "speed", "heading", "satellites"],
    #         "system":              ["heartbeat", "signal_strength"],
    #     },
    # },
    # {
    #     "machine_type": "crane",
    #     "machine_id": "CR-001",
    #     "gps_base": (44.4255, 26.1010),
    #     "sensors": {
    #         "engine":              ["rpm", "temperature", "oil_pressure", "load",
    #                                 "fuel_level", "status"],
    #         "hydraulic":           ["pressure_main", "pressure_tool", "oil_temperature", "oil_level"],
    #         "tool":                ["height", "load", "reach", "rotation", "status"],
    #         "accident_prevention": ["front_distance", "left_distance", "right_distance",
    #                                 "vibration", "alarm"],
    #         "environment":         ["temperature", "wind_speed", "gas_co", "noise_level"],
    #         "gps":                 ["latitude", "longitude", "heading", "satellites"],
    #         "system":              ["heartbeat", "signal_strength"],
    #     },
    # },
    # {
    #     "machine_type": "dumptruck",
    #     "machine_id": "DT-001",
    #     "gps_base": (44.4300, 26.1055),
    #     "sensors": {
    #         "engine":              ["rpm", "temperature", "oil_pressure", "load",
    #                                 "fuel_level", "coolant_temp", "status"],
    #         "transmission":        ["gear", "drive_mode", "gearbox_temp",
    #                                 "left_speed", "right_speed", "torque"],
    #         "pneumatic":           ["brake_pressure", "air_tank_pressure",
    #                                 "brake_status", "parking_brake"],
    #         "tool":                ["angle_pitch", "load", "position", "status"],
    #         "accident_prevention": ["front_distance", "rear_distance", "pitch", "roll", "seatbelt"],
    #         "environment":         ["temperature", "gas_co", "noise_level"],
    #         "gps":                 ["latitude", "longitude", "speed", "heading", "satellites"],
    #         "system":              ["heartbeat", "signal_strength"],
    #     },
    # },
]

_start = time.time()


def elapsed():
    return time.time() - _start


def gen(category, sensor_id, machine):
    gps_lat, gps_lon = machine["gps_base"]
    mt = machine["machine_type"]

    # ── ENGINE ───────────────────────────────────────────────────
    if category == "engine":
        if sensor_id == "rpm":
            return round(random.gauss(1380, 190))
        if sensor_id == "temperature":
            return round(random.gauss(88, 7), 1)
        if sensor_id == "oil_pressure":
            # occasional low-pressure spike for realism
            if random.random() < 0.04:
                return round(random.uniform(1.0, 1.5), 1)   # critical
            return round(random.uniform(2.2, 4.5), 1)
        if sensor_id == "load":
            return round(random.uniform(35, 90), 1)
        if sensor_id == "fuel_level":
            return round(max(8.0, 80.0 - elapsed() * 0.002), 1)
        if sensor_id == "coolant_temp":
            return round(random.gauss(82, 6), 1)
        if sensor_id == "exhaust_temp":
            return round(random.uniform(260, 400), 1)
        if sensor_id == "battery_voltage":
            return round(random.uniform(12.8, 14.4), 1)
        if sensor_id == "alternator":
            return round(random.uniform(13.8, 14.8), 1)
        if sensor_id == "hours":
            return round(1240 + elapsed() / 3600, 1)
        if sensor_id == "status":
            return random.choices(["running", "idle"], weights=[85, 15])[0]

    # ── HYDRAULIC ────────────────────────────────────────────────
    if category == "hydraulic":
        if "pressure" in sensor_id:
            if random.random() < 0.03:
                return round(random.uniform(251, 270), 1)    # critical
            return round(random.uniform(130, 235), 1)
        if sensor_id == "oil_temperature":
            return round(random.gauss(62, 10), 1)
        if sensor_id == "oil_level":
            return round(random.uniform(65, 98), 1)
        if sensor_id == "flow_rate":
            return round(random.uniform(60, 170), 1)
        if sensor_id == "filter_status":
            return random.choices(["ok", "dirty"], weights=[92, 8])[0]

    # ── PNEUMATIC ────────────────────────────────────────────────
    if category == "pneumatic":
        if sensor_id == "brake_pressure":
            return round(random.uniform(6.0, 8.5), 1)
        if sensor_id == "air_tank_pressure":
            return round(random.uniform(6.5, 9.0), 1)
        if sensor_id == "parking_brake_pres":
            return round(random.uniform(5.5, 7.5), 1)
        if sensor_id == "brake_status":
            return random.choices(["released", "engaged"], weights=[80, 20])[0]
        if sensor_id == "parking_brake":
            return random.choices(["off", "on"], weights=[75, 25])[0]
        if sensor_id == "air_dryer_status":
            return "ok"

    # ── TRANSMISSION ─────────────────────────────────────────────
    if category == "transmission":
        if sensor_id in ("left_speed", "right_speed"):
            return round(random.uniform(0, 12), 1)
        if sensor_id in ("left_tension", "right_tension"):
            return round(random.uniform(1.5, 4.5), 1)
        if sensor_id == "gear":
            return random.choice(["N", "1", "2", "3", "R"])
        if sensor_id == "drive_mode":
            return random.choices(["forward", "neutral", "reverse"], weights=[65, 20, 15])[0]
        if sensor_id == "torque":
            return round(random.uniform(300, 900), 1)
        if sensor_id == "gearbox_temp":
            return round(random.gauss(72, 8), 1)
        if sensor_id == "drive_status":
            return random.choices(["ok", "warning"], weights=[95, 5])[0]

    # ── TOOL ─────────────────────────────────────────────────────
    if category == "tool":
        if sensor_id == "angle_pitch":
            return round(random.gauss(0, 8), 1)
        if sensor_id == "angle_tilt":
            return round(random.gauss(0, 5), 1)
        if sensor_id == "height":
            return round(random.uniform(0.2, 8.0), 2)
        if sensor_id == "position":
            return random.choices(["raised", "lowered", "working"], weights=[20, 30, 50])[0]
        if sensor_id == "load":
            return round(random.uniform(10, 200), 1)
        if sensor_id == "reach":
            return round(random.uniform(2.0, 12.0), 2)
        if sensor_id == "rotation":
            return round(random.uniform(-180, 180), 1)
        if sensor_id == "open_angle":
            return round(random.uniform(0, 90), 1)
        if sensor_id == "vibration_freq":
            return round(random.uniform(25, 60), 1)
        if sensor_id == "status":
            return random.choices(["working", "idle", "raised"], weights=[60, 30, 10])[0]

    # ── ACCIDENT PREVENTION ──────────────────────────────────────
    if category == "accident_prevention":
        if "distance" in sensor_id:
            if random.random() < 0.04:
                return round(random.uniform(0.2, 0.5), 2)   # critical
            if random.random() < 0.06:
                return round(random.uniform(0.5, 1.5), 2)   # warning
            return round(random.uniform(1.5, 7.0), 2)
        if sensor_id in ("pitch", "roll", "yaw"):
            return round(random.gauss(0, 5), 1)
        if sensor_id == "vibration":
            return round(random.uniform(0.1, 3.5), 2)
        if sensor_id == "seatbelt":
            return random.choices(["on", "off"], weights=[92, 8])[0]
        if sensor_id == "door_status":
            return random.choices(["closed", "open"], weights=[95, 5])[0]
        if sensor_id in ("camera_front", "camera_rear"):
            return random.choices(["streaming", "offline"], weights=[96, 4])[0]
        if sensor_id == "alarm":
            return random.choices(["none", "proximity_warning"], weights=[90, 10])[0]

    # ── ENVIRONMENT ──────────────────────────────────────────────
    if category == "environment":
        if sensor_id == "temperature":
            return round(random.gauss(22, 4), 1)
        if sensor_id == "humidity":
            return round(random.uniform(30, 80), 1)
        if sensor_id == "altitude":
            return round(random.gauss(82, 8), 1)
        if sensor_id == "gas_co":
            if random.random() < 0.03:
                return round(random.uniform(51, 80), 1)      # critical
            return round(random.uniform(2, 40), 1)
        if sensor_id == "gas_ch4":
            return round(random.uniform(0, 12), 1)
        if sensor_id == "gas_no2":
            return round(random.uniform(0, 18), 1)
        if sensor_id == "air_quality":
            return round(random.uniform(40, 130), 1)
        if sensor_id in ("dust_pm25", "dust_pm10"):
            return round(random.uniform(10, 90), 1)
        if sensor_id == "noise_level":
            return round(random.uniform(72, 108), 1)
        if sensor_id == "wind_speed":
            return round(random.uniform(0, 35), 1)
        if sensor_id == "rain_detected":
            return random.choices(["no", "yes"], weights=[85, 15])[0]

    # ── GPS ──────────────────────────────────────────────────────
    if category == "gps":
        if sensor_id == "latitude":
            return round(gps_lat + random.gauss(0, 0.0003), 6)
        if sensor_id == "longitude":
            return round(gps_lon + random.gauss(0, 0.0003), 6)
        if sensor_id == "altitude":
            return round(random.gauss(85, 3), 1)
        if sensor_id == "speed":
            return round(random.uniform(0, 10), 1)
        if sensor_id == "heading":
            return round(random.uniform(0, 360), 1)
        if sensor_id == "fix":
            return random.choices(["3D", "2D"], weights=[92, 8])[0]
        if sensor_id == "satellites":
            return random.randint(6, 14)
        if sensor_id == "accuracy":
            return round(random.uniform(1.0, 4.5), 1)

    # ── SYSTEM ───────────────────────────────────────────────────
    if category == "system":
        if sensor_id == "heartbeat":
            return "online"
        if sensor_id == "uptime":
            return round(elapsed())
        if sensor_id == "battery":
            return round(random.uniform(3.5, 4.1), 2)
        if sensor_id == "signal_strength":
            return round(random.uniform(-75, -42), 1)
        if sensor_id == "cpu_temperature":
            return round(random.uniform(35, 65), 1)
        if sensor_id == "free_memory":
            return round(random.uniform(50, 200), 1)
        if sensor_id == "firmware_version":
            return "1.4.2"

    return round(random.uniform(0, 100), 2)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[SIM] Conectat la broker {BROKER_HOST}:{BROKER_PORT}")
        print(f"[SIM] Publicare pentru {len(MACHINES)} utilaje la fiecare {PUBLISH_INTERVAL}s\n")
    else:
        print(f"[SIM] Conectare esuata, cod: {rc}")


def on_disconnect(client, userdata, rc):
    print(f"[SIM] Deconectat (cod {rc})")


def main():
    client = mqtt.Client(client_id="machinery_simulator")
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
    time.sleep(1)

    cycle = 0
    while True:
        cycle += 1
        total = sum(len(s) for m in MACHINES for s in m["sensors"].values())
        print(f"--- Ciclu #{cycle} ({total} mesaje) ---")
        for machine in MACHINES:
            mt  = machine["machine_type"]
            mid = machine["machine_id"]
            for category, sensors in machine["sensors"].items():
                for sensor_id in sensors:
                    topic = f"{mt}/{mid}/{category}/{sensor_id}"
                    value = gen(category, sensor_id, machine)
                    client.publish(topic, str(value))
                    print(f"  [{mid}] {category}/{sensor_id:<22} = {value}")
        print()
        time.sleep(PUBLISH_INTERVAL)


if __name__ == "__main__":
    main()