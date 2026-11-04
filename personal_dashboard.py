from src.BASE_MAP import BASE_MAP
import json
from src.database import get_latest_measurement
from src.colors_for_terminal import YELLOW, WHITE, RED, GREEN
from config_manager import configure_stations, CONFIG_FILE
import os
import time

# Hat der User eine json Datei? Wenn nicht, starte config_manager.py
def get_user_stations():
    if not os.path.exists(CONFIG_FILE):
        print("Keine user.config.json gefunden.")
        print("Starte Einrichtung")
        time.sleep(1)

        configure_stations()

        # Falls die Konfigurierung sofort abgebrochen wurde
        if not os.path.exists(CONFIG_FILE):
            print("\n Es wurde keine Konfiguration erstellt. Abbruch.")
            return None

    with open(CONFIG_FILE, "r", encoding="utf-8") as json_file:
        return json.load(json_file)

def print_personal_dashboard():

    user_stations = get_user_stations()
    if not user_stations:
        return

    # Terminal leeren
    print("\033[2J\033[3J\033[H", end="")
    personal_map = BASE_MAP.copy()

    for station in user_stations:

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
    
    for station in user_stations:
        data = get_latest_measurement(station["uuid"])
        
        value = data['value']
        timestamp_str = data['timestamp']
        mean_low_water = data['mean_low_water']
        mean_high_water = data['mean_high_water']
        
        color_code = GREEN
        
        if value != "--" and mean_low_water != "--" and mean_high_water != "--":
            if value > mean_high_water:
                color_code = RED 
            elif value < mean_low_water:
                color_code = YELLOW 
        
        value_text = f"{value:>4} cm    "
               
        value_str = f"{color_code}{value_text}{WHITE}"
        
        print(f"{station['symbol']:<4}   | {station['name']:<24} | {value_str} | {timestamp_str}")

if __name__  == "__main__":
    print_personal_dashboard()
