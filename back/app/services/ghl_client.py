import requests
from django.conf import settings

class GHLClient:
    def __init__(self):
        # BASE URL para GET (sin /v1)
        self.base_url_get = settings.GHL_API_BASE.rstrip("/")

        # BASE URL para POST (con /v1)
        self.base_url_post = self.base_url_get
        if not self.base_url_post.endswith("/v1"):
            self.base_url_post += "/v1"

        self.headers = {
            "Authorization": f"Bearer {settings.GHL_PRIVATE_TOKEN}",
            "Accept": "application/json",
            "Version": "2021-04-15",
        }

    def get_calendars(self):
        location_id = getattr(settings, "GHL_LOCATION_ID", None)
        if not location_id:
            raise ValueError("GHL_LOCATION_ID no está configurado en settings.py")

        url = f"{self.base_url_get}/calendars/"
        params = {"locationId": location_id}
        print(f"📡 URL GET: {url}")
        print(f"🔍 Params: {params}")

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def create_appointment(self, data):
        if getattr(settings, "SIMULATE_GHL", True):
            print("🧪 MODO SIMULACIÓN ACTIVADO")
            print("📦 Payload simulado enviado a GHL:", data)
            return {
                "id": "simulated_appointment_id",
                "calendarId": data.get("calendarId"),
                "contactId": data.get("contactId"),
                "startTime": data.get("startTime"),
                "endTime": data.get("endTime"),
                "message": "Simulación: la cita NO fue enviada a GHL"
            }

        # MODO REAL - HACE LA SOLICITUD
        url = f"{self.base_url_post}/appointments/"
        print(f"🚀 URL POST: {url}")
        print(f"📦 Payload real enviado a GHL: {data}")

        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
