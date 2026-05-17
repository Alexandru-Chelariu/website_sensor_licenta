from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Max
from telemetry.models import SensorReading, MachineSystem
from .forms import AddMachineForm

_CATEGORY_ORDER = [
    "engine", "hydraulic", "pneumatic", "transmission",
    "tool", "environment", "accident_prevention", "gps", "system",
]


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
    all_machines = MachineSystem.objects.all().order_by("machine_type", "machine_id")
    return render(request, "dashboard/machines.html", {
        "machines": all_machines,
        "active_tab": "machines",
        "form": AddMachineForm(),
    })


def add_machine(request):
    if request.method == "POST":
        form = AddMachineForm(request.POST)
        if form.is_valid():
            mid      = form.cleaned_data["machine_id"]
            mtype    = form.cleaned_data["machine_type"]
            label    = form.cleaned_data.get("label") or \
                       f"{dict(MachineSystem.MACHINE_TYPES).get(mtype, mtype)} {mid}"
            location = form.cleaned_data.get("location", "")
            MachineSystem.objects.create(
                system_uid=f"{mtype}-{mid}",
                machine_id=mid,
                machine_type=mtype,
                label=label,
                location=location,
                is_active=False,
            )
            return redirect("machines")
    else:
        form = AddMachineForm()

    return render(request, "dashboard/add_machine.html", {
        "form": form,
        "active_tab": "machines",
    })


def contact(request):
    return render(request, "dashboard/contact.html", {
        "active_tab": "contact",
    })


def machine_status(request, pk):
    machine = get_object_or_404(MachineSystem, pk=pk)

    latest_ids = (
        SensorReading.objects
        .filter(system=machine)
        .values("sensor_id")
        .annotate(max_id=Max("id"))
        .values_list("max_id", flat=True)
    )

    readings = (
        SensorReading.objects
        .filter(id__in=latest_ids)
        .select_related("sensor", "sensor__category")
        .order_by("sensor__sensor_id")
    )

    raw = {}
    gps_lat = gps_lng = None
    readings_data = []

    for reading in readings:
        cat_name = reading.sensor.category.name
        if cat_name not in raw:
            raw[cat_name] = {"label": reading.sensor.category.label, "readings": []}
        raw[cat_name]["readings"].append(reading)

        if cat_name == "gps":
            if reading.sensor.sensor_id == "latitude" and reading.numeric_value is not None:
                gps_lat = float(reading.numeric_value)
            elif reading.sensor.sensor_id == "longitude" and reading.numeric_value is not None:
                gps_lng = float(reading.numeric_value)

        readings_data.append({
            "category": cat_name,
            "sensor_id": reading.sensor.sensor_id,
            "status": reading.status,
        })

    ordered_keys = [c for c in _CATEGORY_ORDER if c in raw] + [c for c in raw if c not in _CATEGORY_ORDER]
    sensors_by_category = {k: raw[k] for k in ordered_keys}

    return render(request, "dashboard/machine_status.html", {
        "machine": machine,
        "sensors_by_category": sensors_by_category,
        "active_tab": "machines",
        "gps_lat": gps_lat,
        "gps_lng": gps_lng,
        "readings_data": readings_data,
    })