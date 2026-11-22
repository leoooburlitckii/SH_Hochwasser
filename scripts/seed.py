import requests
from src.hotspots import HOTSPOTS
from src.stations import STATIONS
from src.database import init_db, save_station

def seed_stations():

    init_db()

    hotspots_uuid = set()

    for hotspot in HOTSPOTS:
        hotspots_uuid.add(hotspot["uuid"])

    for station in STATIONS:
        uuid = station["uuid"]
        name = station["name"]
        row = station["row"]
        col = station["col"]

        mean_high_water = None
        mean_low_water = None

        is_hotspot = uuid in hotspots_uuid 

        url_characteristics = f"https://pegelonline.wsv.de/webservices/rest-api/v2/stations/{uuid}/W.json?includeCharacteristicValues=true"

        try:          
            response_characteristics = requests.get(url_characteristics, timeout = 10)
            if response_characteristics.status_code == 200:
                data_characteristics = response_characteristics.json()
                for thing in data_characteristics["characteristicValues"]:
                    if thing["shortname"] == "MNW" or thing["shortname"] == "MTnw":
                        mean_low_water = thing["value"]
                    if thing["shortname"] == "MHW" or thing["shortname"] == "MThw":
                        mean_high_water = thing["value"]
            else:
                print(f"Fehler bei Station im Durchlauf zu MNW und MHW {name }Statuscode {response_characteristics.status_code}")
                              
        except Exception as e:
            print(f"Fehler bei {e}")

        save_station(
            uuid,
            name,
            mean_low_water,
            mean_high_water,
            col,
            row,
            is_hotspot
        )

if __name__ == "__main__":
    seed_stations()