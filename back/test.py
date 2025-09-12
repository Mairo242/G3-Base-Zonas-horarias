import requests

url = "https://services.leadconnectorhq.com/v1/appointments/"
headers = {
    "Authorization": "Bearer pit-e463b555-10d5-432c-991a-30c4214a5757",
    "Accept": "application/json"
}

data = {
    "calendarId": "tu_calendar_id",
    "contactId": "tu_contact_id",
    "locationId": "tu_location_id",
    "startTime": "2025-09-12T01:00:00+00:00",
    "endTime": "2025-09-12T02:00:00+00:00",
    "title": "Cita de prueba",
    "description": "Probando desde Django"
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.text)
