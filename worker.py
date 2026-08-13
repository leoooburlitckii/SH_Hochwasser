import requests
import time
from database import init_db, save_measurment

STATIONEN = [
    {
        "name": "LÜBECK-BAUHOF",
        "uuid" : "f4f9f7fb-eeff-46dc-9727-04d8aa56240a"
    },

    {
        "name": "TRAVEMÜNDE",
        "uuid" : "c7383149-1f77-430d-8bef-c5667be3846b"
    },

    {
        "name": "LIST AUF SYLT",
        "uuid" : "5e92d73f-e4ea-42c1-9f98-91536c17cdff"
    },

    {
        "name": "HÖRNUM",
        "uuid" : "733755fd-628f-4130-a694-aaba340531ba"
    },

    {
        "name": "WITTDÜN",
        "uuid" : "9c4c11f2-0548-4555-beac-ecfd36f9bd74"
    },

    {
        "name": "PELLWORM ANLEGER",
        "uuid" : "2852b9ab-d30e-4d04-ae06-3e946f48a0b1"
    },

    {
        "name": "HUSUM",
        "uuid" : "e114aeec-c8d9-4d20-8fe1-8822058cb38b"
    },

    {
        "name": "FLENSBURG",
        "uuid" : "9e19c411-f728-4a43-a057-39d4155c71cc"
    },

    {
        "name": "LANGBALLIGAU",
        "uuid" : "5a33bf14-6bdc-4666-b2e3-ac78e3083e2a"
    },

    {
        "name": "SCHLESWIG",
        "uuid" : "09370c05-1041-4395-a5d4-b8db6e59c4c8"
    },

    {
        "name": "KAPPELN",
        "uuid" : "b09f2243-60f0-469a-8f3b-0ea6abc83267"
    },

    {
        "name": "ECKERNFÖRDE",
        "uuid" : "1faa9b2c-c269-4662-af70-ef11da27cc1c"
    },

    {
        "name": "LT KIEL",
        "uuid" : "736437d7-0f6f-41b7-bc69-5ed721da4f85"
    },

    {
        "name": "MARIENLEUCHTE",
        "uuid" : "8effc15d-8583-4ac6-9f42-1b63c47f92b0"
    },

    {
        "name": "HEILIGENHAFEN",
        "uuid" : "06219dd9-a2c4-463c-9619-623b3c026cbc"
    },

    {
        "name": "NEUSTADT",
        "uuid" : "3f0b6b74-80a9-4576-a3cb-ea967dfc349f"
    },

    {
        "name": "BÜSSAU UP",
        "uuid" : "bf7bb8e8-e81f-4655-9e84-28738feae936"
    },

    {
        "name": "KIEL-HOLTENAU",
        "uuid" : "3ad4013f-644b-47f5-a641-44b332bfecb2"
    },

    {
        "name": "NOK KIEL AUSSEN",
        "uuid" : "6dc44585-5b88-45d7-9c64-7c845408b698"
    },

    {
        "name": "NOK KIEL BINNEN",
        "uuid" : "8af24d6a-eecd-434e-9f1a-60ab6bc05490"
    },

    {
        "name": "AWK STROHBRÜCK",
        "uuid" : "0e192297-1224-4465-b1c7-a476cc17f74d"
    },

    {
        "name": "NOK KÖNIGSFÖRDE",
        "uuid" : "d0ec2790-a870-405e-bb61-2dcc3cf47467"
    },

    {
        "name": "NOK RENDSBURG",
        "uuid" : "8c8afb56-88ea-483a-a7d4-033c22f53497"
    },

    {
        "name": "NOK BREIHOLZ",
        "uuid" : "4a904d59-d48f-4878-af7b-cbd955f342e0"
    },

    {
        "name": "LEXFÄHRE OBERWASSER",
        "uuid" : "86c5688f-2fac-4d58-a245-ad8ce14cafbf"
    },

    {
        "name": "LEXFÄHRE UNTERWASSER",
        "uuid" : "7f01fbd8-653c-40ba-8ed0-57386a9b4557"
    },
    
    {
        "name": "BÜSUM",
        "uuid" : "5287a3e1-c540-4ab1-b52e-880d124cbc43"
    },

    {
        "name": "TÖNNING",
        "uuid" : "00e386ac-e35c-4a6e-80dd-f8cd8a9e7a62"
    },

    {
        "name": "FRIEDRICHSTADT STRASSENBRÜCKE",
        "uuid" : "721313e7-935a-4bb8-8c6d-0e014211b2ec"
    },

    {
        "name": "FRIEDRICHSTADT TREENE",
        "uuid" : "795ce865-3ac4-43b8-88d5-049a34e4359e"
    },

    {
        "name": "NORDFELD OBERWASSER",
        "uuid" : "61394669-3f1b-44e5-ae37-50fd2512f4fa"
    },

    {
        "name": "NORDFELD UNTERWASSER",
        "uuid" : "cb93548e-c1ce-43f6-b3a1-6903f8835b33"
    },

    {
        "name": "EIDER-SPERRWERK BP",
        "uuid" : "8ac85e6c-6167-496c-b16f-fa94f81cd94a"
    },

    {
        "name": "EIDER-SPERRWERK AP",
        "uuid" : "04acd7e5-3cbc-4cdd-b4a9-f452e868f4d6"
    },

    {
        "name": "NOK DÜKERSWISCH",
        "uuid" : "3954300d-f112-4fe6-8d0a-b06496372e36"
    },

    {
        "name": "NOK BRUNSBÜTTEL",
        "uuid" : "85fc0dac-a53f-4638-880d-40b24bb282f3"
    },

    {
        "name": "BRUNSBÜTTEL MPM",
        "uuid" : "d4f5f719-8c52-4f8d-945d-1c31404cc628"
    },

    {
        "name": "GW-PWDRFP 02",
        "uuid" : "e1217d07-91f8-4019-b3a2-0c0d69316ab8"
    },

    {
        "name": "GW-PWDRFP 01",
        "uuid" : "4a4daad2-0e96-4070-914e-a1c4f6b7a3e5"
    },

    {
        "name": "GW-PWDRFP 03",
        "uuid" : "6cb287c2-2fb2-4845-b11f-e78bd5db2ce3"
    },

    {
        "name": "GW-PWDRFP 08",
        "uuid" : "bc9f369e-5fd4-466c-8d97-ddb1ecd2aed2"
    },

    {
        "name": "GW-PWDRFP 09",
        "uuid" : "18216ff8-18aa-4a71-bd32-e7479ccc439d"
    },

    {
        "name": "GW-PWDRFP 04",
        "uuid" : "6e19aeca-d37a-4b00-9354-c6dd90f12de2"
    },

    {
        "name": "GW-PWDRFP 06",
        "uuid" : "69fc0432-e9dc-400c-8c21-0c26e85df884"
    },

    {
        "name": "GW-PWDRFP 07",
        "uuid" : "f6dc9514-bdaf-4817-b3bf-34cd4b5c3e18"
    },

    {
        "name": "GRÖNHUDE",
        "uuid" : "15859426-834c-429e-9c41-2e097b717b1d"
    },

    {
        "name": "BREITENBERG",
        "uuid" : "24c6a014-864b-4d53-bd05-0b49106f5412"
    },

    {
        "name": "ITZEHOE HAFEN",
        "uuid" : "d863cbc3-5e5e-4095-855c-026f0850dd58"
    },

    {
        "name": "BROKDORF",
        "uuid" : "610ab204-d3c4-4a11-a38b-e31461fdcf27"
    },

    {
        "name": "STÖR-SPERRWERK AP",
        "uuid" : "d9acdbec-61ff-4308-978a-2f4d1c2c4059"
    },

    {
        "name": "GLÜCKSTADT",
        "uuid" : "1f1bbed7-c1fa-45b4-90d3-df94b50ad631"
    },

    {
        "name": "KOLLMAR",
        "uuid" : "3ed90357-4b01-4119-b1c5-bd2c62871e7b"
    },

    {
        "name": "KRÜCKAU-SPERRWERK AP",
        "uuid" : "a653eb04-de2e-47f7-8e2c-09277cfe95ae"
    },

    {
        "name": "ELMSHORN HAFEN",
        "uuid" : "136febf6-1371-4118-a9b8-4275444bda5d"
    },

    {
        "name": "PINNAU-SPERRWERK AP",
        "uuid" : "391bbba5-83d4-4791-b07e-65ab29b423f6"
    },

    {
        "name": "UETERSEN",
        "uuid" : "575da86f-d975-4837-b6f5-6f19c3a5e4b6"
    },

    {
        "name": "HETLINGEN",
        "uuid" : "599c23b1-4550-41e3-a7e7-3056989927f1"
    },

    {
        "name": "SCHULAU",
        "uuid" : "f3c6ee73-5561-4068-96ec-364016e7d9ef"
    },

    {
        "name": "HELGOLAND SÜDHAFEN",
        "uuid" : "0d8233b8-36c9-4a24-ad77-a4e7c617932f"
    },

    {
        "name": "HELGOLAND BINNENHAFEN",
        "uuid" : "c0ec139b-13b4-4f86-bee3-06665ad81a40"
    },

    {
        "name": "HOHNSTORF",
        "uuid" : "d9289367-c8aa-4b6a-b1ad-857fec94c6bb"
    },

    {
        "name": "GEESTHACHT",
        "uuid" : "44f7e955-c97d-45c8-9ed7-19406806fb4c"
    },

    {
        "name": "DONNERSCHLEUSE OP",
        "uuid" : "45634232-36ac-416c-806d-5f64201dae2c"
    },

    {
        "name": "MÖLLN",
        "uuid" : "46644438-83d6-4da8-a2a1-1deb2cb67561"
    }
   
]

def fetch_and_store():
    print("\n Update gestartet")
    for station in STATIONEN:
        uuid = station["uuid"]
        name = station["name"]

        url = f"https://pegelonline.wsv.de/webservices/rest-api/v2/stations/{uuid}/W/currentmeasurement.json"

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                save_measurment(
                    station_uuid=uuid,
                    station_name=name,
                    wasserstand=data["value"],
                    zeitstempel=data["timestamp"]
                )
            else:
                print(f"Fehler bei Station {name }Statuscode {response.status_code}")
        except Exception as e:
            print(f"Fehler bei {e}")

if __name__ == "__main__":
    init_db()
    print("Worker.py läuft")
    while True:
        fetch_and_store()

        WAIT_SECONDS = 900
        print(f"Es wird {WAIT_SECONDS} bis zu nächsten Aktualisierung gewartet")
        time.sleep(WAIT_SECONDS)