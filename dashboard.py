from database import get_latest_measurment
from hotspots import HOTSPOTS
from colors_for_terminal import YELLOW, WHITE, RED, GREEN


def print_dashboard():

    # Leert den Terminal-Bildschirm (\033[2J), löscht den Scroll-Puffer/Historie (\033[3J) 
    # und setzt den Cursor nach oben links (\033[H), ohne eine neue Zeile anzuhängen (end="")
    print("\033[2J\033[3J\033[H", end="")


    karte = """
    =======================================================================
                    SCHLESWIG-HOLSTEIN PEGELLOGGER
    =======================================================================
        11                                                                
        ▒                                                                     
               ▒▒▒▒▒▒▒▒▒                                                      
                ▒▒▒▒▒▒▒▒▒▒▒▒▒   ▒ 4 ▒                                         
                 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   ▒                                
           ▒▒▒    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                                
        ▒           ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                               
                     ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                               
                     ▒8▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒7▒▒▒▒▒▒▒▒                               
                    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒9                           ▒▒▒▒▒   
                      ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                     ▒▒▒▒  
                ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒3▒▒▒▒▒▒▒                    
               ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    ▒▒▒▒▒       
                      ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒      
                    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒       
                    ▒ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒          
                       ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒             
                     ▒ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒              
                     ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒           
                       ▒ ▒▒▒▒▒▒▒▒▒▒▒▒▒6▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒            
                               ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒2              
                                ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒1▒              
                                  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒             
                                    ▒▒▒▒▒▒▒▒▒▒▒    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒          
                                    ▒▒▒▒▒▒▒▒       ▒▒▒▒▒▒▒▒▒▒▒10▒▒▒▒          
                                                  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒            
                                                    ▒▒▒▒▒▒▒▒▒▒▒▒▒             
                                                      ▒5▒▒▒▒▒                 
                                                          ▒▒▒         
    """
    print(karte)
    # Header: Exakt abgestimmte Breiten (NR=4, STATION=24, WASSERSTAND=12)
    print(f"{'NR':<4}   | {'STATION':<24} | {'WASSERSTAND':<11} | {'ZEITSTEMPEL'}")
    print("-" * 78)
    print(f"Farben: {YELLOW}[Gelb = Niedrigwasser]{WHITE}, {GREEN}[Grün = Normal]{WHITE}, {RED}[Rot = Hochwasser]{WHITE}")
    print("-" * 78)

    for hotspot in HOTSPOTS:
        daten = get_latest_measurment(hotspot["uuid"])

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

        print(f"{hotspot['nr']:<4}   | {hotspot['name']:<24} | {wert_str} | {zeit_str}")

    print("=" * 78)

if __name__  == "__main__":
    print_dashboard()
