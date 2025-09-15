# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
import requests
from django.conf import settings  # para leer SIMULATE_GHL y GHL_PRIVATE_TOKEN


def get_calendars(request):
    try:
        from .services.ghl_client import GHLClient
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
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            print("📩 Datos recibidos:", data)

            if settings.SIMULATE_GHL:
                return JsonResponse({"message": "Simulación: cita creada", "data": data}, status=201)

            # Armamos el payload SOLO con los campos requeridos
            payload = {
                "calendarId": data["calendarId"],
                "contactId": data["contactId"],
                "locationId": data["locationId"],
                "startTime": data["startTime"],
                "endTime": data["endTime"],
            }

            headers = {
                "Authorization": f"Bearer {settings.GHL_PRIVATE_TOKEN}",
                "Content-Type": "application/json",
                "Version": "2021-07-28",
            }

            GHL_API_URL = f"{settings.GHL_API_BASE}/calendars/events/appointments"

            print("📡 Intentando POST a:", GHL_API_URL)
            print("📤 Payload:", payload)

            response = requests.post(GHL_API_URL, headers=headers, json=payload)
            print("📥 Respuesta GHL:", response.status_code, response.text)

            try:
                return JsonResponse(response.json(), status=response.status_code)
            except Exception:
                return JsonResponse({
                    "error": "Respuesta no JSON",
                    "status": response.status_code,
                    "body": response.text
                }, status=response.status_code)

        except Exception as e:
            tb = traceback.format_exc()
            print("❌ Error en create_appointment:", e)
            print(tb)
            return JsonResponse({"error": str(e), "traceback": tb}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)
