# mqtt_client/topics.py

# ─────────────────────────────────────────────────────────────
# Categorii de senzori — comune pentru toate tipurile de utilaje
# ─────────────────────────────────────────────────────────────

SENSOR_CATEGORIES = [
    "tool",           # Scula / unealta principala (lama, cupa, ciocan, carlig etc.)
    "environment",    # Factori de mediu
    "engine",         # Motor
    "accident_prevention",  # Proximitate, camera, IMU, inclinare
    "hydraulic",      # Sistem hidraulic
    "pneumatic",      # Sistem pneumatic / frâne
    "transmission",   # Transmisie, senile, roti
    "gps",            # Localizare
    "system",         # Sistem ESP/Arduino (baterie, semnal, heartbeat)
]

# ─────────────────────────────────────────────────────────────
# SENSOR DEFINITIONS
# cheie: sensor_id folosit in topic
# valori: unit, numeric, description
# ─────────────────────────────────────────────────────────────

SENSORS = {

    # ── TOOL (Scula principala) ───────────────────────────────
    "tool": {
        "angle_pitch":    {"unit": "°",   "numeric": True,  "desc": "Inclinare față-spate sculă"},
        "angle_tilt":     {"unit": "°",   "numeric": True,  "desc": "Basculare stânga-dreapta sculă"},
        "height":         {"unit": "m",   "numeric": True,  "desc": "Înălțime față de sol"},
        "position":       {"unit": "",    "numeric": False, "desc": "Poziție sculă (raised/lowered/working)"},
        "load":           {"unit": "kN",  "numeric": True,  "desc": "Forță exercitată de sculă"},
        "reach":          {"unit": "m",   "numeric": True,  "desc": "Raza de acțiune (excavator/macara)"},
        "rotation":       {"unit": "°",   "numeric": True,  "desc": "Unghi rotație (excavator)"},
        "open_angle":     {"unit": "°",   "numeric": True,  "desc": "Unghi deschidere cupa/graifer"},
        "vibration_freq": {"unit": "Hz",  "numeric": True,  "desc": "Frecvență vibrare (compactor/ciocan)"},
        "status":         {"unit": "",    "numeric": False, "desc": "Status sculă"},
    },

    # ── ENVIRONMENT ───────────────────────────────────────────
    "environment": {
        "temperature":    {"unit": "°C",    "numeric": True,  "desc": "Temperatură ambientală"},
        "humidity":       {"unit": "%",     "numeric": True,  "desc": "Umiditate relativă"},
        "altitude":       {"unit": "m",     "numeric": True,  "desc": "Altitudine barometrică"},
        "gas_co":         {"unit": "ppm",   "numeric": True,  "desc": "Monoxid de carbon"},
        "gas_ch4":        {"unit": "ppm",   "numeric": True,  "desc": "Metan"},
        "gas_no2":        {"unit": "ppm",   "numeric": True,  "desc": "Dioxid de azot"},
        "air_quality":    {"unit": "AQI",   "numeric": True,  "desc": "Indice calitate aer"},
        "dust_pm25":      {"unit": "µg/m³", "numeric": True,  "desc": "Particule PM2.5"},
        "dust_pm10":      {"unit": "µg/m³", "numeric": True,  "desc": "Particule PM10"},
        "noise_level":    {"unit": "dB",    "numeric": True,  "desc": "Nivel zgomot"},
        "wind_speed":     {"unit": "km/h",  "numeric": True,  "desc": "Viteza vântului"},
        "rain_detected":  {"unit": "",      "numeric": False, "desc": "Ploaie detectată (yes/no)"},
    },

    # ── ENGINE ────────────────────────────────────────────────
    "engine": {
        "rpm":            {"unit": "RPM",  "numeric": True,  "desc": "Turatie motor"},
        "temperature":    {"unit": "°C",   "numeric": True,  "desc": "Temperatură motor"},
        "oil_pressure":   {"unit": "bar",  "numeric": True,  "desc": "Presiune ulei motor"},
        "load":           {"unit": "%",    "numeric": True,  "desc": "Incărcare motor"},
        "fuel_level":     {"unit": "%",    "numeric": True,  "desc": "Nivel combustibil"},
        "coolant_temp":   {"unit": "°C",   "numeric": True,  "desc": "Temperatură lichid răcire"},
        "exhaust_temp":   {"unit": "°C",   "numeric": True,  "desc": "Temperatură gaze evacuare"},
        "battery_voltage":{"unit": "V",    "numeric": True,  "desc": "Tensiune baterie"},
        "alternator":     {"unit": "V",    "numeric": True,  "desc": "Tensiune alternator"},
        "hours":          {"unit": "h",    "numeric": True,  "desc": "Ore funcționare motor"},
        "status":         {"unit": "",     "numeric": False, "desc": "Status motor (running/idle/off/fault)"},
    },

    # ── ACCIDENT PREVENTION ───────────────────────────────────
    "accident_prevention": {
        "front_distance": {"unit": "m",  "numeric": True,  "desc": "Distanță obstacol față"},
        "rear_distance":  {"unit": "m",  "numeric": True,  "desc": "Distanță obstacol spate"},
        "left_distance":  {"unit": "m",  "numeric": True,  "desc": "Distanță obstacol stânga"},
        "right_distance": {"unit": "m",  "numeric": True,  "desc": "Distanță obstacol dreapta"},
        "camera_front":   {"unit": "",   "numeric": False, "desc": "Status cameră față"},
        "camera_rear":    {"unit": "",   "numeric": False, "desc": "Status cameră spate"},
        "pitch":          {"unit": "°",  "numeric": True,  "desc": "Inclinare față-spate utilaj"},
        "roll":           {"unit": "°",  "numeric": True,  "desc": "Inclinare lateral utilaj"},
        "yaw":            {"unit": "°",  "numeric": True,  "desc": "Rotație verticală"},
        "vibration":      {"unit": "m/s²","numeric": True, "desc": "Vibrații șasiu"},
        "seatbelt":       {"unit": "",   "numeric": False, "desc": "Centură de siguranță (on/off)"},
        "door_status":    {"unit": "",   "numeric": False, "desc": "Status ușă cabină"},
        "alarm":          {"unit": "",   "numeric": False, "desc": "Alarmă activă"},
    },

    # ── HYDRAULIC ─────────────────────────────────────────────
    "hydraulic": {
        "pressure_main":  {"unit": "bar",   "numeric": True, "desc": "Presiune circuit principal"},
        "pressure_tool":  {"unit": "bar",   "numeric": True, "desc": "Presiune cilindri sculă"},
        "pressure_lift":  {"unit": "bar",   "numeric": True, "desc": "Presiune cilindru ridicare"},
        "pressure_tilt":  {"unit": "bar",   "numeric": True, "desc": "Presiune cilindru basculare"},
        "pressure_c1":    {"unit": "bar",   "numeric": True, "desc": "Presiune cilindru 1"},
        "pressure_c2":    {"unit": "bar",   "numeric": True, "desc": "Presiune cilindru 2"},
        "pressure_c3":    {"unit": "bar",   "numeric": True, "desc": "Presiune cilindru 3"},
        "pressure_c4":    {"unit": "bar",   "numeric": True, "desc": "Presiune cilindru 4"},
        "oil_temperature":{"unit": "°C",    "numeric": True, "desc": "Temperatură ulei hidraulic"},
        "oil_level":      {"unit": "%",     "numeric": True, "desc": "Nivel ulei hidraulic"},
        "flow_rate":      {"unit": "L/min", "numeric": True, "desc": "Debit ulei hidraulic"},
        "filter_status":  {"unit": "",      "numeric": False,"desc": "Status filtru hidraulic"},
    },

    # ── PNEUMATIC ─────────────────────────────────────────────
    "pneumatic": {
        "brake_pressure":     {"unit": "bar", "numeric": True,  "desc": "Presiune frâne de serviciu"},
        "air_tank_pressure":  {"unit": "bar", "numeric": True,  "desc": "Presiune rezervor aer"},
        "parking_brake_pres": {"unit": "bar", "numeric": True,  "desc": "Presiune frână de parcare"},
        "brake_status":       {"unit": "",    "numeric": False, "desc": "Status frâne (engaged/released/fault)"},
        "parking_brake":      {"unit": "",    "numeric": False, "desc": "Frână parcare (on/off)"},
        "air_dryer_status":   {"unit": "",    "numeric": False, "desc": "Status uscat aer"},
    },

    # ── TRANSMISSION ──────────────────────────────────────────
    "transmission": {
        "left_speed":       {"unit": "km/h", "numeric": True,  "desc": "Viteză șenilă/roată stânga"},
        "right_speed":      {"unit": "km/h", "numeric": True,  "desc": "Viteză șenilă/roată dreapta"},
        "left_tension":     {"unit": "bar",  "numeric": True,  "desc": "Tensiune șenilă stânga"},
        "right_tension":    {"unit": "bar",  "numeric": True,  "desc": "Tensiune șenilă dreapta"},
        "gear":             {"unit": "",     "numeric": False, "desc": "Treaptă de viteză"},
        "drive_mode":       {"unit": "",     "numeric": False, "desc": "Mod deplasare (forward/reverse/neutral)"},
        "torque":           {"unit": "Nm",   "numeric": True,  "desc": "Cuplu transmisie"},
        "gearbox_temp":     {"unit": "°C",   "numeric": True,  "desc": "Temperatură cutie de viteze"},
        "drive_status":     {"unit": "",     "numeric": False, "desc": "Status transmisie"},
    },

    # ── GPS ───────────────────────────────────────────────────
    "gps": {
        "latitude":   {"unit": "°",    "numeric": True,  "desc": "Latitudine"},
        "longitude":  {"unit": "°",    "numeric": True,  "desc": "Longitudine"},
        "altitude":   {"unit": "m",    "numeric": True,  "desc": "Altitudine GPS"},
        "speed":      {"unit": "km/h", "numeric": True,  "desc": "Viteză GPS"},
        "heading":    {"unit": "°",    "numeric": True,  "desc": "Direcție (0-360)"},
        "fix":        {"unit": "",     "numeric": False, "desc": "Status fix GPS"},
        "satellites": {"unit": "",     "numeric": True,  "desc": "Nr. sateliți"},
        "accuracy":   {"unit": "m",    "numeric": True,  "desc": "Precizie poziție"},
    },

    # ── SYSTEM ────────────────────────────────────────────────
    "system": {
        "heartbeat":        {"unit": "",    "numeric": False, "desc": "Semnal de viață"},
        "uptime":           {"unit": "s",   "numeric": True,  "desc": "Timp funcționare sistem"},
        "battery":          {"unit": "V",   "numeric": True,  "desc": "Tensiune baterie ESP/Arduino"},
        "signal_strength":  {"unit": "dBm", "numeric": True,  "desc": "Putere semnal WiFi/GSM"},
        "cpu_temperature":  {"unit": "°C",  "numeric": True,  "desc": "Temperatură procesor IoT"},
        "free_memory":      {"unit": "KB",  "numeric": True,  "desc": "Memorie liberă ESP"},
        "firmware_version": {"unit": "",    "numeric": False, "desc": "Versiune firmware"},
    },
}

# ─────────────────────────────────────────────────────────────
# TIPURI DE UTILAJE + senzorii specifici (in plus fata de comuni)
# ─────────────────────────────────────────────────────────────

MACHINE_TYPES = {
    "bulldozer": {
        "label": "Buldozer",
        "specific_sensors": {
            "tool": ["angle_pitch", "angle_tilt", "height", "position", "load"],
            "transmission": ["left_speed", "right_speed", "left_tension", "right_tension", "drive_status"],
        }
    },
    "excavator": {
        "label": "Excavator",
        "specific_sensors": {
            "tool": ["angle_pitch", "rotation", "reach", "open_angle", "load", "status"],
            "hydraulic": ["pressure_c1", "pressure_c2", "pressure_c3", "pressure_c4"],
        }
    },
    "crane": {
        "label": "Macara",
        "specific_sensors": {
            "tool": ["height", "load", "reach", "rotation", "status"],
            "accident_prevention": ["front_distance", "left_distance", "right_distance", "vibration"],
        }
    },
    "compactor": {
        "label": "Compactor",
        "specific_sensors": {
            "tool": ["vibration_freq", "load", "height", "status"],
        }
    },
    "grader": {
        "label": "Greder",
        "specific_sensors": {
            "tool": ["angle_pitch", "angle_tilt", "height", "load"],
        }
    },
    "loader": {
        "label": "Incărcător frontal",
        "specific_sensors": {
            "tool": ["angle_pitch", "height", "load", "open_angle", "status"],
        }
    },
    "dumptruck": {
        "label": "Autobasculantă",
        "specific_sensors": {
            "tool": ["angle_pitch", "load", "position", "status"],
            "transmission": ["gear", "drive_mode", "gearbox_temp"],
        }
    },
    "piledriver": {
        "label": "Pilot de batere piloți",
        "specific_sensors": {
            "tool": ["height", "load", "vibration_freq", "status"],
        }
    },
    "concrete_pump": {
        "label": "Pompă beton",
        "specific_sensors": {
            "tool": ["height", "reach", "rotation", "status"],
            "hydraulic": ["pressure_main", "pressure_tool", "flow_rate"],
        }
    },
}

# ─────────────────────────────────────────────────────────────
# FORMAT TOPIC MQTT
# {machine_type}/{machine_id}/{category}/{sensor_id}
# Exemplu: bulldozer/BD-001/engine/rpm
# ─────────────────────────────────────────────────────────────

def build_topic(machine_type: str, machine_id: str, category: str, sensor_id: str) -> str:
    return f"{machine_type}/{machine_id}/{category}/{sensor_id}"


def get_all_topics_for_machine(machine_type: str, machine_id: str) -> list:
    topics = []
    for category, sensors in SENSORS.items():
        for sensor_id in sensors:
            topics.append(build_topic(machine_type, machine_id, category, sensor_id))
    return topics


# ── CONTROL & ALERTS ─────────────────────────────────────────
CONTROL_TOPIC_TEMPLATE = "{machine_type}/{machine_id}/control/cmd"
ALERT_TOPIC_TEMPLATE   = "{machine_type}/{machine_id}/alerts"