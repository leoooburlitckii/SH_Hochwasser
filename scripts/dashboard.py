from src.database import get_latest_measurement
from src.database import get_hotspots
from src.colors_for_terminal import YELLOW, WHITE, RED, GREEN


def print_dashboard():

    # Leert den Terminal-Bildschirm (\033[2J), löscht den Scroll-Puffer/Historie (\033[3J)
    # und setzt den Cursor nach oben links (\033[H), ohne eine neue Zeile anzuhängen (end="")
    print("\033[2J\033[3J\033[H", end="")


    map_text = """
    =======================================================================
                    SCHLESWIG-HOLSTEIN PEGELLOGGER
    =======================================================================
  11
  ▒
  ▒      ▒▒▒▒▒▒▒▒▒
          ▒▒▒▒▒▒▒▒▒▒▒▒▒   ▒   ▒
           ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒4▒▒▒▒▒▒▒▒   ▒
     ▒▒▒    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
  ▒           ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
               ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
       ▒▒       ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒7▒▒▒▒▒▒▒▒▒
            ▒▒  8▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒9                           ▒▒▒▒▒
                ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                     ▒▒▒▒
          ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒3▒▒▒▒▒▒▒                    
         ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    ▒▒▒▒▒
                ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
              ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
              ▒ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
                 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
               ▒ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
               ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒6▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
                 ▒ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒            
                         ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒2              
                          ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒1▒
                            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
                              ▒▒▒▒▒▒▒▒▒▒▒    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
                              ▒▒▒▒▒▒▒▒       ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
                                            ▒▒▒▒▒▒▒▒▒10▒▒▒▒▒
                                              ▒▒▒▒▒▒▒▒▒▒▒▒▒
                                                ▒5▒▒▒▒▒
                                                    ▒▒▒                 
    """
    print(map_text)
    
    print(f"{'NR':<4}   | {'STATION':<24} | {'WASSERSTAND':<11} | {'ZEITSTEMPEL'}")
    print("-" * 78)
    print(f"Farben: {YELLOW}[Gelb = Niedrigwasser]{WHITE}, {GREEN}[Grün = Normal]{WHITE}, {RED}[Rot = Hochwasser]{WHITE}")
    print("-" * 78)

    hotspots = get_hotspots()
    
    for idx, hotspot in enumerate(hotspots, start = 1):
        data = get_latest_measurement(hotspot.uuid)

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

        print(f"{idx:<4}   | {hotspot.name:<24} | {value_str} | {timestamp_str}")

    print("=" * 78)

if __name__  == "__main__":
    print_dashboard()
