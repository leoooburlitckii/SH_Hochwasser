import requests
import time
from src.database import init_db, save_measurment, get_all_stations
from datetime import datetime


def fetch_and_store():
    print("\n Update gestartet")
    stationen = get_all_stations()
    for station in stationen:
        uuid = station.uuid
        name = station.name

        url = f"https://pegelonline.wsv.de/webservices/rest-api/v2/stations/{uuid}/W/currentmeasurement.json"
        
        try:
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                parsed_datatime = datetime.fromisoformat(data["timestamp"])
                
                save_measurment(
                    station_uuid=uuid,
                    station_name=name,
                    wasserstand=data["value"],
                    zeitstempel=parsed_datatime
                )
            else:
                print(f"Fehler bei Station {name }Statuscode {response.status_code}")
        except Exception as e:
            print(f"Fehler bei {e}")

if __name__ == "__main__":
    init_db()
    print("Worker.py läuft")
    while True:
        fetch_and_store()

        WAIT_SECONDS = 900
        print(f"Es wird {WAIT_SECONDS} bis zu nächsten Aktualisierung gewartet")
        time.sleep(WAIT_SECONDS)