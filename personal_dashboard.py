from BASE_MAP import BASE_MAP
import json
from database import get_latest_measurment
from colors_for_terminal import YELLOW, WHITE, RED, GREEN


def print_personal_dashboard():

    personal_map = BASE_MAP.copy()

    with open("user_config.json", "r") as json_file:
        selected_stations = json.load(json_file)

    for station in selected_stations:

        row = station["row"]
        col = station["col"]
        num = station["symbol"]
        personal_map[row] = personal_map[row][:col] + num + personal_map[row][col+1:]


    print("""
    =======================================================================
                        SCHLESWIG-HOLSTEIN PEGELLOGGER
    =======================================================================
    
    """)
    for row in personal_map:
        print(row)

    print("\n")
    print(f"{'NR':<4}   | {'STATION':<24} | {'WASSERSTAND':<11} | {'ZEITSTEMPEL'}")
    print("-" * 78)
    print(f"Farben: {YELLOW}[Gelb = Niedrigwasser]{WHITE}, {GREEN}[Grün = Normal]{WHITE}, {RED}[Rot = Hochwasser]{WHITE}")
    print("-" * 78)
    
    for station in selected_stations:
        daten = get_latest_measurment(station["uuid"])
        
        wert = daten['wert']
        zeit_str = daten['zeit']
        mnw = daten['mnw']
        mhw = daten['mhw']
        
        farbcode = GREEN
        
        if wert != "--" and mnw is not None and mhw is not None:
            if wert > mhw:
                farbcode = RED 
            elif wert < mnw:
                farbcode = YELLOW 
        
        wert_text = f"{wert:>4} cm    "
               
        wert_str = f"{farbcode}{wert_text}{WHITE}"
        
        print(f"{station['symbol']:<4}   | {station['name']:<24} | {wert_str} | {zeit_str}")

if __name__  == "__main__":
    print_personal_dashboard()
