# serializers.py
from rest_framework import serializers
from datetime import datetime
from zoneinfo import ZoneInfo  # ✅ Librería moderna de zonas horarias

class CalendarSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    status = serializers.CharField()

class AppointmentSerializer(serializers.Serializer):
    calendarId = serializers.CharField(required=True)
    contactId = serializers.CharField(required=True)
    startTime = serializers.DateTimeField(required=True)
    endTime = serializers.DateTimeField(required=True)
    
    def validate(self, data):
        # Convertir a UTC antes de enviar a GHL
        lima_tz = ZoneInfo('America/Lima')
        utc_tz = ZoneInfo('UTC')
        
        # Asumir que las horas recibidas están en zona horaria de Perú
        start_time = data['startTime']
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=lima_tz)
        data['startTime'] = start_time.astimezone(utc_tz)
        
        end_time = data['endTime']
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=lima_tz)
        data['endTime'] = end_time.astimezone(utc_tz)
        
        return data