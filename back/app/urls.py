# back/app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("calendars/", views.get_calendars, name="get_calendars"),
    path("appointments/create/", views.create_appointment, name="create_appointment"),
]