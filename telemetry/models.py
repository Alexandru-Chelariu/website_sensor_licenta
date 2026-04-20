# telemetry/models.py

from django.db import models


class MachineSystem(models.Model):
    MACHINE_TYPES = [
        ("bulldozer",      "Buldozer"),
        ("excavator",      "Excavator"),
        ("crane",          "Macara"),
        ("compactor",      "Compactor"),
        ("grader",         "Auto-Greder"),
        ("loader",         "Incărcător frontal"),
        ("dumptruck",      "Autobasculantă"),
        ("piledriver",     "Pilot batere piloți"),
        ("concrete_pump",  "Pompă beton"),
        ("other",          "Alt utilaj"),
    ]

    system_uid    = models.CharField(max_length=64, unique=True)
    machine_type  = models.CharField(max_length=32, choices=MACHINE_TYPES)
    machine_id    = models.CharField(max_length=32)
    label         = models.CharField(max_length=100)
    firmware      = models.CharField(max_length=32, blank=True)
    location      = models.CharField(max_length=200, blank=True)
    is_active     = models.BooleanField(default=True)
    last_seen     = models.DateTimeField(null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["machine_type", "machine_id"]

    def __str__(self):
        return f"[{self.machine_type.upper()}] {self.machine_id} — {self.label}"


class SensorCategory(models.Model):
    CATEGORY_CHOICES = [
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

    name  = models.CharField(max_length=32, choices=CATEGORY_CHOICES, unique=True)
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label


class Sensor(models.Model):
    category    = models.ForeignKey(SensorCategory, on_delete=models.CASCADE,
                                    related_name="sensors")
    sensor_id   = models.CharField(max_length=64)
    label       = models.CharField(max_length=100)
    unit        = models.CharField(max_length=16, blank=True)
    is_numeric  = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("category", "sensor_id")
        ordering = ["category", "sensor_id"]

    def __str__(self):
        unit_str = f" ({self.unit})" if self.unit else ""
        return f"{self.category} / {self.sensor_id}{unit_str}"


class SensorReading(models.Model):
    STATUS_CHOICES = [
        ("normal",   "Normal"),
        ("warning",  "Avertizare"),
        ("critical", "Critic"),
        ("fault",    "Defect"),
        ("unknown",  "Necunoscut"),
    ]
    system      = models.ForeignKey(MachineSystem, on_delete=models.CASCADE,
                                    related_name="readings")
    sensor      = models.ForeignKey(Sensor, on_delete=models.CASCADE,
                                    related_name="readings")
    raw_value     = models.CharField(max_length=256)
    numeric_value = models.FloatField(null=True, blank=True)
    unit          = models.CharField(max_length=16, blank=True)
    status      = models.CharField(max_length=16, choices=STATUS_CHOICES, default="normal")
    topic       = models.CharField(max_length=256)
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-received_at"]
        indexes = [
            models.Index(fields=["system", "sensor", "-received_at"]),
            models.Index(fields=["received_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return (
            f"{self.system.machine_id} | "
            f"{self.sensor.category} / {self.sensor.sensor_id} | "
            f"{self.raw_value} {self.unit} | "
            f"{self.received_at:%Y-%m-%d %H:%M:%S}"
        )