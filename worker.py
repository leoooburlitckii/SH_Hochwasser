import requests
import time
from database import init_db, save_measurment

STATIONEN = [
    {
        "name": "LÜBECK-BAUHOF",
        "uuid" : "f4f9f7fb-eeff-46dc-9727-04d8aa56240a"
    },
    {
        "name": "TRAVEMÜNDE",
        "uuid" : "c7383149-1f77-430d-8bef-c5667be3846b"
    }   
]

def fetch_and_store():
    print("\n Update gestartet")
    for station in STATIONEN:
        uuid = station["uuid"]
        name = station["name"]

        url = "https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{uuid}/W/currentmeasurement.json"

        