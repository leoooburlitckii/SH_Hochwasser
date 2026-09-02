import json
from stations import STATIONEN

CONFIG_FILE = "user_config.json"

def configure_stations():
    print("=" * 60)


    for idx, station in enumerate(STATIONEN, start=1):
        print(f"[{idx:>2}] {station['name']:<30}", end="\n" if idx % 2 == 0 else "  ")
    
    print("-" * 60)
    print("Wähle Stationen nacheinander aus. (Leere Eingabe zum Beenden)")
    
    selected_list = []
    used_symbols = set()
    used_stations = set()

    #Station wählen
    while True:
        choice = input("\n Stationsnummer eingeben (Enter=Fertig): ").strip()
        if not choice:
            break

        if not choice.isdigit() or not (1 <= int(choice) <= len(STATIONEN)):
            print("Ungültige Eingabe, wiederholen Sie")
            continue

        
        idx = int(choice) -1
        st = STATIONEN[idx]
        if st["uuid"] in used_stations:
            print(f"{st['name']} wurde bereits hinzugefügt")
            continue

        #Symbol wählen
        while True:
            symbol = input(f"1 Zeichen Symbol für {st['name']} eingeben: ").strip()
            if len(symbol) != 1:
                print("Ungültige Eingabe, Wiederholen Sie")
            elif symbol in used_symbols:
                print(f"Symbol {symbol} wird schon für eine andere Station verwendet")
            else:
                break

        used_symbols.add(symbol)
        used_stations.add(st["uuid"])

        selected_list.append({
            "symbol" :symbol,
            "name": st["name"],
            "uuid": st["uuid"],
            "row": st["row"],
            "col": st["col"]
            
        })

        print(f"Station {st['name']} mit Symbol {symbol} hinzugefügt")

    if selected_list:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(selected_list, f, indent=4, ensure_ascii=False)
        print(f"\n{len(selected_list)} Stationen erfolgreich in '{CONFIG_FILE}' gespeichert!")
    else:
        print("\nKeine Änderungen gespeichert.")

if __name__  == "__main__":
    configure_stations()