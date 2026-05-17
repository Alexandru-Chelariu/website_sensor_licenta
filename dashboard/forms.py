# -*- coding: utf-8 -*-
from django import forms
from telemetry.models import MachineSystem


class AddMachineForm(forms.Form):
    machine_id = forms.CharField(
        max_length=32,
        label="Numar serial ESP32",
        widget=forms.TextInput(attrs={"placeholder": "ex: BD-001", "autocomplete": "off"}),
    )
    machine_type = forms.ChoiceField(
        choices=[("", "-- Selecteaza tipul --")] + MachineSystem.MACHINE_TYPES,
        label="Tip utilaj",
    )
    label = forms.CharField(
        max_length=100,
        required=False,
        label="Nume afisat",
        widget=forms.TextInput(attrs={"placeholder": "ex: Buldozer Sector 3 (optional)"}),
    )
    location = forms.CharField(
        max_length=200,
        required=False,
        label="Locatie",
        widget=forms.TextInput(attrs={"placeholder": "ex: Santier Bd. Unirii (optional)"}),
    )

    def clean_machine_id(self):
        return self.cleaned_data["machine_id"].strip().upper()

    def clean_machine_type(self):
        val = self.cleaned_data.get("machine_type", "")
        if not val:
            raise forms.ValidationError("Selecteaza tipul utilajului.")
        return val

    def clean(self):
        cleaned = super().clean()
        mid = cleaned.get("machine_id")
        mtype = cleaned.get("machine_type")
        if mid and mtype:
            if MachineSystem.objects.filter(system_uid=f"{mtype}-{mid}").exists():
                self.add_error(
                    "machine_id",
                    f"Serialul {mid} cu tipul selectat este deja inregistrat.",
                )
        return cleaned
