from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("machines/", views.machines, name="machines"),
    path("contact/", views.contact, name="contact"),
]