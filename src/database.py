import sqlite3

def init_db():

    db = sqlite3.connect('sh_hochwasser.db')
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messungen (
        station_uuid TEXT PRIMARY KEY,
        station_name TEXT NOT NULL,
        wasserstand INTEGER NOT NULL,
        zeitstempel TEXT NOT NULL,
        MNW REAL,
        MHW REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        station_name TEXT NOT NULL,
        schwellenwert TEXT NOT NULL
    )
    """)

    db.commit()
    db.close()

def save_measurment(station_uuid: str ,station_name: str, wasserstand: int, zeitstempel: str, mnw: float=None, mhw: float =None):

    db = sqlite3.connect('sh_hochwasser.db')
    cursor = db.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO messungen (station_uuid, station_name, wasserstand, zeitstempel, MNW, MHW)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (station_uuid, station_name, wasserstand, zeitstempel, mnw, mhw))

    db.commit()
    db.close()
    print(f" Gespeichert {station_name} mit {station_uuid}-> {wasserstand}cm {zeitstempel}, {mnw} cm und {mhw} cm")


def get_latest_measurment(station_uuid: str ):

    db = sqlite3.connect('sh_hochwasser.db')
    cursor = db.cursor()

    cursor.execute("""
        SELECT station_name, wasserstand, zeitstempel, mnw, mhw
        FROM messungen
        WHERE station_uuid = ?
    """, (station_uuid,))

    result = cursor.fetchone()
    db.close()

    if result:
        return {
            "name": result[0],
            "wert": result[1],
            "zeit": result[2],
            "mnw": result[3],
            "mhw": result[4]
        }

    return {
        "name": "Unbekannt",
        "wert": "--",
        "zeit": "--",
        "mnw": "--",
        "mhw": "--"
    }