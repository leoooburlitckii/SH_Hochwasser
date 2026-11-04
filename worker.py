import requests
import time
from src.database import init_db, save_measurements_batch, get_all_stations
from datetime import datetime


def fetch_and_store():
    print("\nUpdate gestartet")
    stations = get_all_stations()
    for station in stations:
        uuid = station.uuid
        name = station.name

        url = f"https://pegelonline.wsv.de/webservices/rest-api/v2/stations/{uuid}/W/measurements.json?start=P31D"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            measurements = response.json()
            valid_measurements = []

            for measurement in measurements:
                try:
                    if "value" not in measurement or "timestamp" not in measurement:
                        continue

                    parsed_datetime = datetime.fromisoformat(measurement["timestamp"])
                    valid_measurements.append({
                        "value": measurement["value"],
                        "timestamp": parsed_datetime
                    })
                except (ValueError, KeyError):
                    continue

            if valid_measurements:
                count = save_measurements_batch(uuid, valid_measurements)
                print(f"Station {name}: {count} Messungen gespeichert")
            else:
                print(f"Station {name}: keine gültigen Messungen")

        except requests.RequestException as e:
            print(f"Netzwerkfehler bei {name}: {e}")
        except Exception as e:
            print(f"Fehler bei {name}: {e}")

if __name__ == "__main__":
    init_db()
    print("Worker.py läuft - lädt 31 Tage Daten pro Durchlauf")
    while True:
        fetch_and_store()

        WAIT_SECONDS = 900
        print(f"Es wird {WAIT_SECONDS}s bis zur nächsten Aktualisierung gewartet")
        time.sleep(WAIT_SECONDS)