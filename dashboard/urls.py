from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("machines/", views.machines, name="machines"),
    path("machines/add/", views.add_machine, name="add_machine"),
    path("machines/<int:pk>/", views.machine_status, name="machine_status"),
    path("contact/", views.contact, name="contact"),
]