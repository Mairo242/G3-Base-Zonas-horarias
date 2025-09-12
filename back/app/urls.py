# back/app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('calendars/', views.get_calendars, name='ghl_calendars'),
    path('appointments/create/', views.create_appointment, name='ghl_create_appointment'),
]