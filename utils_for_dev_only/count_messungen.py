import requests

from src.stations import STATIONEN

BASE_URL = "https://pegelonline.wsv.de/webservices/rest-api/v2/stations"


def count_measurements(uuid: str) -> int:
    # One request: all measurements of the last 31 days (ISO 8601 period P31D)
    url = f"{BASE_URL}/{uuid}/W/measurements.json?start=P31D"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return len(response.json())


def main():
    total = 0

    for station in STATIONEN:
        try:
            count = count_measurements(station["uuid"])
        except requests.RequestException as e:
            print(f"{station['name']}: Netzwerkfehler ({e})")
            continue

        total += count
        print(f"{station['name']}: {count} Messungen")

    print(f"\nStationen: {len(STATIONEN)}, Messungen insgesamt: {total}")


if __name__ == "__main__":
    main()
