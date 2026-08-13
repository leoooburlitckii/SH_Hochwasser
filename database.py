import sqlite3

def init_db():
    db = sqlite3.connect('sh_hochwasser.db')

    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messungen (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_uuid TEXT NOT NULL,
        station_name TEXT NOT NULL,
        wasserstand INTEGER NOT NULL,
        zeitstempel TEXT NOT NULL
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

def save_measurment(station_uuid: str ,station_name: str, wasserstand: int, zeitstempel: int):

    db = sqlite3.connect('sh_hochwasser.db')
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO messungen (station_uuid, station_name, wasserstand, zeitstempel)
        VALUES (?,?, ?, ?)
    """, (station_uuid, station_name, wasserstand, zeitstempel))

    db.commit()
    db.close()
    print(f" Gespeichert {station_name} mit {station_uuid}-> {wasserstand}cm {zeitstempel}")
    