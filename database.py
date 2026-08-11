import sqlite3

db = sqlite3.connect('sh_hochwasser.db')

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messungen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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

