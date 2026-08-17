import requests
import json

# 1. Wir definieren die URL, die wir fragen wollen.
# Das hier ist die URL für die aktuelle Messung am Pegel "LÜBECK-BAUHOF" (der ist direkt in der Altstadt)
#url = "https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/f4f9f7fb-eeff-46dc-9727-04d8aa56240a/W/currentmeasurement.json"
url = "https://pegelonline.wsv.de/webservices/rest-api/v2/stations/f4f9f7fb-eeff-46dc-9727-04d8aa56240a/W.json?includeCharacteristicValues=true"
# 2. Wir schicken unseren Kellner (requests) los, um die Daten zu holen
antwort = requests.get(url)

# 3. Wir prüfen, ob die Antwort erfolgreich war (Statuscode 200 heißt "Alles OK")
if antwort.status_code == 200:
    print("✅ Anfrage erfolgreich!")
    
    # 4. Wir wandeln die Text-Antwort in ein Python-Dictionary (JSON) um
    daten = antwort.json()
    
    # 5. Wir lassen uns die Daten hübsch formatiert ausgeben
    print("Das sind die rohen Daten vom Server:")
    print(json.dumps(daten, indent=4, ensure_ascii=False))
    
    # 6. Jetzt greifen wir gezielt auf die Werte zu, die wir brauchen
    
    #wert = daten["value"]
    #zeit = daten["timestamp"]
    
    #print(f"\n🌊 Der aktuelle Wasserstand am Bauhof ist {wert} cm.")
    #print(f"🕒 Gemessen am: {zeit}")
    
#else:
    #print(f"❌ Fehler bei der Anfrage. Statuscode: {antwort.status_code}")