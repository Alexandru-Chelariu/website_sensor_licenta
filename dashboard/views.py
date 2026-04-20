from django.shortcuts import render
from telemetry.models import SensorReading, MachineSystem


def home(request):
    recent_readings = (
        SensorReading.objects
        .select_related("system", "sensor", "sensor__category")
        .order_by("-received_at")[:20]
    )
    machines = MachineSystem.objects.filter(is_active=True).order_by("machine_type")

    return render(request, "dashboard/home.html", {
        "recent_readings": recent_readings,
        "machines": machines,
        "active_tab": "home",
    })


def machines(request):
    machines = MachineSystem.objects.all().order_by("machine_type", "machine_id")
    return render(request, "dashboard/machines.html", {
        "machines": machines,
        "active_tab": "machines",
    })


def contact(request):
    return render(request, "dashboard/contact.html", {
        "active_tab": "contact",
    })