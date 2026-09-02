from BASE_MAP import BASE_MAP
import json
from database import get_latest_measurment
from colors_for_terminal import YELLOW, WHITE, RED, GREEN
from config_manager import configure_stations, CONFIG_FILE
import os
import time

# hat der user json datei? wenn nicht starte config_manager.py
def get_user_stations():
    if not os.path.exists(CONFIG_FILE):
        print("Keine user.config.json gefunden.")
        print("Starte Einrichtung")
        time.sleep(1)

        configure_stations()

        #Falls Konfigurierung sofort abgebrochen wurde
        if not os.path.exists(CONFIG_FILE):
            print("\n Es wurde keine Konfiguration erstellt. Abbruch.")
            return None

    with open(CONFIG_FILE, "r", encoding="utf-8") as json_file:
        return json.load(json_file)

def print_personal_dashboard():

    user_stations = get_user_stations()
    if not user_stations:
        return

    #Terminal leeren
    print("\033[2J\033[3J\033[H", end="")
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
