# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from .services.ghl_client import GHLClient
import traceback

def get_calendars(request):
    try:
        client = GHLClient()
        calendars_data = client.get_calendars()
        
        calendar_list = calendars_data.get("calendars", [])
        
        filtered_calendars = []
        for calendar in calendar_list:
            filtered_calendars.append({
                'id': calendar.get('id'),
                'name': calendar.get('name'),
                'status': calendar.get('status', 'active')
            })
        
        return JsonResponse(filtered_calendars, safe=False)
        
    except Exception as e:
        tb = traceback.format_exc()
        print("Error en get_calendars:", e)
        print(tb)
        return JsonResponse({'error': str(e), 'traceback': tb}, status=500)

@csrf_exempt
def create_appointment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            required_fields = ['calendarId', 'contactId', 'locationId', 'startTime', 'endTime']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'error': f'Campo requerido: {field}'}, status=400)
            
            lima_tz = ZoneInfo('America/Lima')
            utc_tz = ZoneInfo('UTC')
            
            start_time_naive = datetime.fromisoformat(data['startTime'])
            start_time_lima = start_time_naive.replace(tzinfo=lima_tz)
            start_time_utc = start_time_lima.astimezone(utc_tz)
            
            end_time_naive = datetime.fromisoformat(data['endTime'])
            end_time_lima = end_time_naive.replace(tzinfo=lima_tz)
            end_time_utc = end_time_lima.astimezone(utc_tz)
            
            appointment_data = {
                'calendarId': data['calendarId'],
                'contactId': data['contactId'],
                'locationId': data['locationId'],
                'startTime': start_time_utc.isoformat(),
                'endTime': end_time_utc.isoformat(),
                'title': data.get('title', 'Cita creada desde Django'),
                'description': data.get('description', ''),
            }
            
            print("📦 Payload final enviado a GHL:", appointment_data)
            
            client = GHLClient()
            appointment_response = client.create_appointment(appointment_data)
            
            print("📥 Respuesta cruda de GHL:", appointment_response)

            response_data = {
                'id': appointment_response.get('id'),
                'calendarId': appointment_response.get('calendarId'),
                'contactId': appointment_response.get('contactId'),
                'startTimeUTC': start_time_utc.strftime('%Y-%m-%d %H:%M:%S UTC'),
                'endTimeUTC': end_time_utc.strftime('%Y-%m-%d %H:%M:%S UTC'),
                'startTimeLima': start_time_lima.strftime('%Y-%m-%d %H:%M:%S %Z'),
                'endTimeLima': end_time_lima.strftime('%Y-%m-%d %H:%M:%S %Z'),
                'message': 'Cita creada exitosamente en GHL'
            }
            
            print("📤 Response final:", response_data)

            return JsonResponse(response_data, status=201)
            
        except ValueError as e:
            return JsonResponse({'error': f'Formato de fecha inválido: {str(e)}'}, status=400)
        except Exception as e:
            tb = traceback.format_exc()
            print("Error en create_appointment:", e)
            print(tb)
            return JsonResponse({'error': str(e), 'traceback': tb}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
