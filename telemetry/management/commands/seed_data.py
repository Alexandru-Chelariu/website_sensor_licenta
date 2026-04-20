import random
from datetime import datetime, timedelta, timezone

from django.core.management.base import BaseCommand
from django.utils import timezone as dj_timezone

from telemetry.models import MachineSystem, SensorCategory, Sensor, SensorReading


# ── Date de baza ──────────────────────────────────────────────────────────────

MACHINES = [
    {"system_uid": "ESP-BD-001", "machine_type": "bulldozer",  "machine_id": "BD-001", "label": "Buldozer Șantier Nord"},
    {"system_uid": "ESP-EX-042", "machine_type": "excavator",  "machine_id": "EX-042", "label": "Excavator Sector 2"},
    {"system_uid": "ESP-CR-007", "machine_type": "crane",      "machine_id": "CR-007", "label": "Macara Turn A"},
    {"system_uid": "ESP-DT-015", "machine_type": "dumptruck",  "machine_id": "DT-015", "label": "Autobasculantă 15"},
]

CATEGORIES = [
    ("tool",                "Sculă / Unealtă"),
    ("environment",         "Mediu înconjurător"),
    ("engine",              "Motor"),
    ("accident_prevention", "Prevenire accidente"),
    ("hydraulic",           "Sistem hidraulic"),
    ("pneumatic",           "Sistem pneumatic"),
    ("transmission",        "Transmisie"),
    ("gps",                 "GPS / Localizare"),
    ("system",              "Sistem IoT"),
]

SENSOR_DEFS = {
    "engine": [
        ("rpm",          "Turație motor",         "RPM",   True),
        ("temperature",  "Temperatură motor",      "°C",    True),
        ("oil_pressure", "Presiune ulei",          "bar",   True),
        ("load",         "Încărcare motor",        "%",     True),
        ("fuel_level",   "Nivel combustibil",      "%",     True),
        ("coolant_temp", "Temp. lichid răcire",    "°C",    True),
        ("status",       "Status motor",           "",      False),
    ],
    "hydraulic": [
        ("pressure_main",  "Presiune circuit",    "bar",   True),
        ("pressure_blade", "Presiune cilindri",   "bar",   True),
        ("pressure_lift",  "Presiune ridicare",   "bar",   True),
        ("oil_temperature","Temp. ulei hidraulic","°C",    True),
        ("oil_level",      "Nivel ulei hidraulic","%",     True),
        ("flow_rate",      "Debit ulei",          "L/min", True),
    ],
    "pneumatic": [
        ("brake_pressure",    "Presiune frâne",    "bar",  True),
        ("air_tank_pressure", "Rezervor aer",      "bar",  True),
        ("brake_status",      "Status frâne",      "",     False),
        ("parking_brake",     "Frână parcare",     "",     False),
    ],
    "tool": [
        ("angle_pitch", "Inclinare față-spate", "°",  True),
        ("angle_tilt",  "Basculare lateral",    "°",  True),
        ("height",      "Înălțime față de sol", "m",  True),
        ("position",    "Poziție sculă",        "",   False),
        ("load",        "Forță sculă",          "kN", True),
    ],
    "accident_prevention": [
        ("front_distance", "Distanță față",     "m",    True),
        ("rear_distance",  "Distanță spate",    "m",    True),
        ("left_distance",  "Distanță stânga",   "m",    True),
        ("right_distance", "Distanță dreapta",  "m",    True),
        ("pitch",          "Inclinare utilaj",  "°",    True),
        ("roll",           "Ruliu utilaj",      "°",    True),
        ("vibration",      "Vibrații",          "m/s²", True),
        ("camera_front",   "Cameră față",       "",     False),
        ("camera_rear",    "Cameră spate",      "",     False),
    ],
    "environment": [
        ("temperature", "Temp. ambientală",  "°C",    True),
        ("humidity",    "Umiditate",         "%",     True),
        ("altitude",    "Altitudine",        "m",     True),
        ("gas_co",      "CO (monoxid carbon)","ppm",  True),
        ("gas_ch4",     "CH4 (metan)",       "ppm",   True),
        ("air_quality", "Calitate aer AQI",  "AQI",   True),
        ("dust_pm25",   "Praf PM2.5",        "µg/m³", True),
    ],
    "transmission": [
        ("left_speed",   "Viteză stânga",   "km/h", True),
        ("right_speed",  "Viteză dreapta",  "km/h", True),
        ("left_tension", "Tensiune stânga", "bar",  True),
        ("right_tension","Tensiune dreapta","bar",  True),
        ("drive_status", "Status transmisie","",    False),
    ],
    "gps": [
        ("latitude",   "Latitudine",   "°",    True),
        ("longitude",  "Longitudine",  "°",    True),
        ("altitude",   "Altitudine",   "m",    True),
        ("speed",      "Viteză GPS",   "km/h", True),
        ("heading",    "Direcție",     "°",    True),
        ("fix",        "Fix GPS",      "",     False),
        ("satellites", "Sateliți",     "",     True),
    ],
    "system": [
        ("heartbeat",       "Semnal viață",    "",    False),
        ("uptime",          "Timp funcționare","s",   True),
        ("battery",         "Baterie ESP",     "V",   True),
        ("signal_strength", "Semnal WiFi",     "dBm", True),
    ],
}


def random_value(sensor_id, category, is_numeric):
    """Generează o valoare realistă pentru fiecare senzor."""
    if not is_numeric:
        text_values = {
            "status":       ["running", "running", "idle", "fault"],
            "brake_status": ["released", "released", "engaged", "fault"],
            "parking_brake":["off", "off", "on"],
            "position":     ["working", "working", "raised", "lowered"],
            "drive_status": ["forward", "forward", "neutral", "reverse", "fault"],
            "camera_front": ["streaming", "streaming", "offline"],
            "camera_rear":  ["streaming", "streaming", "offline"],
            "fix":          ["fixed", "fixed", "searching"],
            "heartbeat":    ["online"],
        }
        options = text_values.get(sensor_id, ["ok", "active", "normal"])
        return random.choice(options), None

    numeric_ranges = {
        # engine
        "rpm":            (700,  2200),
        "temperature":    (75,   105),
        "oil_pressure":   (2.0,  5.5),
        "load":           (30,   95),
        "fuel_level":     (20,   100),
        "coolant_temp":   (75,   100),
        "exhaust_temp":   (300,  600),
        "battery_voltage":(23,   27),
        "alternator":     (27,   29),
        "hours":          (100,  5000),
        # hydraulic
        "pressure_main":  (120,  250),
        "pressure_blade": (80,   220),
        "pressure_lift":  (70,   200),
        "pressure_tilt":  (60,   190),
        "pressure_c1":    (60,   200),
        "pressure_c2":    (60,   200),
        "pressure_c3":    (60,   200),
        "pressure_c4":    (60,   200),
        "oil_temperature":(40,   80),
        "oil_level":      (50,   100),
        "flow_rate":      (20,   80),
        # pneumatic
        "brake_pressure":     (5.5, 9.0),
        "air_tank_pressure":  (7.0, 11.0),
        "parking_brake_pres": (6.0, 9.0),
        # tool
        "angle_pitch":    (-20,  20),
        "angle_tilt":     (-15,  15),
        "height":         (-0.5, 1.5),
        "reach":          (2,    15),
        "rotation":       (-180, 180),
        "open_angle":     (0,    90),
        "vibration_freq": (10,   60),
        # accident prevention
        "front_distance": (0.2,  8.0),
        "rear_distance":  (0.2,  8.0),
        "left_distance":  (0.2,  6.0),
        "right_distance": (0.2,  6.0),
        "pitch":          (-20,  20),
        "roll":           (-15,  15),
        "vibration":      (0.1,  5.0),
        # environment
        "humidity":       (20,   90),
        "altitude":       (80,   200),
        "gas_co":         (0,    30),
        "gas_ch4":        (0,    10),
        "gas_no2":        (0,    5),
        "air_quality":    (15,   100),
        "dust_pm25":      (5,    80),
        "dust_pm10":      (10,   120),
        "noise_level":    (55,   95),
        "wind_speed":     (0,    30),
        # transmission
        "left_speed":     (0,    12),
        "right_speed":    (0,    12),
        "left_tension":   (1.5,  4.5),
        "right_tension":  (1.5,  4.5),
        "torque":         (200,  900),
        "gearbox_temp":   (40,   90),
        # gps
        "latitude":       (44.40, 44.45),
        "longitude":      (26.05, 26.15),
        "speed":          (0,    12),
        "heading":        (0,    360),
        "satellites":     (6,    14),
        "accuracy":       (1,    8),
        # system
        "uptime":         (0,    86400),
        "battery":        (22,   26),
        "signal_strength":(-80,  -40),
        "cpu_temperature":(35,   65),
        "free_memory":    (80,   200),
    }

    lo, hi = numeric_ranges.get(sensor_id, (0, 100))
    if isinstance(lo, float) or isinstance(hi, float):
        val = round(random.uniform(lo, hi), 2)
    else:
        val = random.randint(int(lo), int(hi))
    return str(val), float(val)


def get_status(sensor_id, category, numeric_value, raw_value):
    if raw_value in ["fault", "error", "offline", "lost"]:
        return "fault"
    if category == "engine":
        if sensor_id == "temperature" and numeric_value and numeric_value > 100:
            return "critical"
        if sensor_id == "oil_pressure" and numeric_value and numeric_value < 2.0:
            return "critical"
        if sensor_id == "fuel_level" and numeric_value and numeric_value < 20:
            return "warning"
    if category == "accident_prevention":
        if "distance" in sensor_id and numeric_value:
            if numeric_value < 0.5:  return "critical"
            if numeric_value < 1.5:  return "warning"
    if category == "hydraulic":
        if "pressure" in sensor_id and numeric_value and numeric_value > 230:
            return "warning"
    if category == "pneumatic":
        if "pressure" in sensor_id and numeric_value and numeric_value < 5.0:
            return "critical"
    if category == "environment":
        if sensor_id == "gas_co" and numeric_value and numeric_value > 25:
            return "critical"
        if sensor_id == "air_quality" and numeric_value and numeric_value > 80:
            return "warning"
    return "normal"


class Command(BaseCommand):
    help = "Populează baza de date cu date dummy pentru testare"

    def add_arguments(self, parser):
        parser.add_argument(
            "--readings", type=int, default=200,
            help="Număr de citiri per mașinuță (default: 200)"
        )
        parser.add_argument(
            "--clear", action="store_true",
            help="Șterge datele existente înainte de seed"
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Șterg datele existente...")
            SensorReading.objects.all().delete()
            MachineSystem.objects.all().delete()
            self.stdout.write(self.style.WARNING("Date șterse."))

        readings_count = options["readings"]

        # 1. Creează categorii
        self.stdout.write("Creez categorii senzori...")
        cat_objs = {}
        for name, label in CATEGORIES:
            cat, _ = SensorCategory.objects.get_or_create(name=name, defaults={"label": label})
            cat_objs[name] = cat

        # 2. Creează senzori
        self.stdout.write("Creez definiții senzori...")
        sensor_objs = {}
        for cat_name, sensors in SENSOR_DEFS.items():
            cat = cat_objs[cat_name]
            for sensor_id, label, unit, is_numeric in sensors:
                sensor, _ = Sensor.objects.get_or_create(
                    category=cat,
                    sensor_id=sensor_id,
                    defaults={"label": label, "unit": unit, "is_numeric": is_numeric}
                )
                sensor_objs[(cat_name, sensor_id)] = sensor

        # 3. Creează mașini
        self.stdout.write("Creez utilaje...")
        machine_objs = []
        for m in MACHINES:
            machine, _ = MachineSystem.objects.get_or_create(
                system_uid=m["system_uid"],
                defaults={
                    "machine_type": m["machine_type"],
                    "machine_id":   m["machine_id"],
                    "label":        m["label"],
                    "is_active":    True,
                    "last_seen":    dj_timezone.now(),
                }
            )
            machine_objs.append(machine)

        # 4. Creează citiri
        self.stdout.write(f"Generez {readings_count} citiri per utilaj...")
        now = dj_timezone.now()
        all_readings = []

        for machine in machine_objs:
            for i in range(readings_count):
                # Timp random în ultimele 24h
                offset = timedelta(seconds=random.randint(0, 86400))
                ts = now - offset

                # Sensor random
                cat_name = random.choice(list(SENSOR_DEFS.keys()))
                sensor_id, *_ = random.choice(SENSOR_DEFS[cat_name])
                sensor = sensor_objs.get((cat_name, sensor_id))
                if not sensor:
                    continue

                raw, numeric = random_value(sensor_id, cat_name, sensor.is_numeric)
                status = get_status(sensor_id, cat_name, numeric, raw)
                topic = f"{machine.machine_type}/{machine.machine_id}/{cat_name}/{sensor_id}"

                all_readings.append(SensorReading(
                    system=machine,
                    sensor=sensor,
                    raw_value=raw,
                    numeric_value=numeric,
                    unit=sensor.unit,
                    status=status,
                    topic=topic,
                    received_at=ts,
                ))

        SensorReading.objects.bulk_create(all_readings)

        total = len(all_readings)
        self.stdout.write(self.style.SUCCESS(
            f"\n✓ Seed complet!"
            f"\n  Utilaje:   {len(machine_objs)}"
            f"\n  Senzori:   {len(sensor_objs)}"
            f"\n  Citiri:    {total}"
        ))