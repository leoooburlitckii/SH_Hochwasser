import requests
import time
from database import init_db, save_measurment
from stations import STATIONEN


def fetch_and_store():
    print("\n Update gestartet")
    for station in STATIONEN:
        uuid = station["uuid"]
        name = station["name"]

        url = f"https://pegelonline.wsv.de/webservices/rest-api/v2/stations/{uuid}/W/currentmeasurement.json"

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                save_measurment(
                    station_uuid=uuid,
                    station_name=name,
                    wasserstand=data["value"],
                    zeitstempel=data["timestamp"]
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