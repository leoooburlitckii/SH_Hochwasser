import requests
from src.hotspots import HOTSPOTS
from src.stations import STATIONEN
from src.database import init_db, save_station

def seed_stations():

    init_db()

    hotspots_uuid = set()

    for hotspot in HOTSPOTS:
        hotspots_uuid.add(hotspot["uuid"])

    for station in STATIONEN:
        uuid = station["uuid"]
        name = station["name"]
        row = station["row"]
        col = station["col"]

        mhw = None
        mnw = None

        is_hotspot = uuid in hotspots_uuid 

        url_mnw_mhw = f"https://pegelonline.wsv.de/webservices/rest-api/v2/stations/{uuid}/W.json?includeCharacteristicValues=true"

        try:          
            response_mnw_mhw = requests.get(url_mnw_mhw, timeout = 10)
            if response_mnw_mhw.status_code == 200:
                data_mnw_mhw = response_mnw_mhw.json()
                for thing in data_mnw_mhw["characteristicValues"]:
                    if thing["shortname"] == "MNW" or thing["shortname"] == "MTnw":
                        mnw = thing["value"]
                    if thing["shortname"] == "MHW" or thing["shortname"] == "MThw":
                        mhw = thing["value"]
            else:
                print(f"Fehler bei Station im Durchlauf zu MNW und MHW {name }Statuscode {response_mnw_mhw.status_code}")
                              
        except Exception as e:
            print(f"Fehler bei {e}")

        save_station(
            uuid,
            name,
            mnw,
            mhw,
            col,
            row,
            is_hotspot
        )

if __name__ == "__main__":
    seed_stations()