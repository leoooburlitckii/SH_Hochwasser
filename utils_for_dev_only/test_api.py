import random

import requests

from src.stations import STATIONS

BASE_URL = "https://pegelonline.wsv.de/webservices/rest-api/v2/stations"


def main():
    # Pick exactly one random station from the list
    station = random.choice(STATIONS)
    print(f"Station: {station['name']} ({station['uuid']})")

    # One single request: all measurements of the last 31 days (ISO 8601 period P31D)
    url = f"{BASE_URL}/{station['uuid']}/W/measurements.json?start=P31D"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    measurements = response.json()  # list of {"timestamp": ..., "value": ...}

    print(f"Anzahl Messungen: {len(measurements)}")
    if not measurements:
        print("Keine Daten erhalten.")
        return

    values = [m["value"] for m in measurements]
    print(f"Erste Messung:  {measurements[0]['timestamp']}  {measurements[0]['value']} cm")
    print(f"Letzte Messung: {measurements[-1]['timestamp']}  {measurements[-1]['value']} cm")
    print(f"Minimum: {min(values)} cm")
    print(f"Maximum: {max(values)} cm")


if __name__ == "__main__":
    main()
