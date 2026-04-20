# telemetry/admin.py
from django.contrib import admin
from .models import MachineSystem, SensorCategory, Sensor, SensorReading


@admin.register(MachineSystem)
class MachineSystemAdmin(admin.ModelAdmin):
    list_display  = ["machine_id", "machine_type", "label", "is_active", "last_seen", "registered_at"]
    list_filter   = ["machine_type", "is_active"]
    search_fields = ["machine_id", "label", "system_uid"]
    ordering      = ["machine_type", "machine_id"]


@admin.register(SensorCategory)
class SensorCategoryAdmin(admin.ModelAdmin):
    list_display  = ["name", "label"]
    ordering      = ["name"]


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display  = ["sensor_id", "category", "label", "unit", "is_numeric"]
    list_filter   = ["category", "is_numeric"]
    search_fields = ["sensor_id", "label"]
    ordering      = ["category", "sensor_id"]


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display  = [
        "id",
        "get_machine_id",
        "get_category",
        "get_sensor_id",
        "raw_value",
        "unit",
        "status",
        "received_at",       # <-- numele corect
    ]
    list_filter   = [
        "sensor__category",  # <-- corect, prin FK
        "status",
        "received_at",       # <-- numele corect
        "system__machine_type",
    ]
    search_fields = [
        "system__machine_id",
        "sensor__sensor_id",
        "topic",
        "raw_value",
    ]
    ordering      = ["-received_at"]  # <-- numele corect
    readonly_fields = ["received_at", "topic"]

    @admin.display(description="Machine ID")
    def get_machine_id(self, obj):
        return obj.system.machine_id

    @admin.display(description="Category")
    def get_category(self, obj):
        return obj.sensor.category.name

    @admin.display(description="Sensor")
    def get_sensor_id(self, obj):
        return obj.sensor.sensor_id