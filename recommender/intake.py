import sqlite3

def fetch_intake():
    conn = sqlite3.connect("./db/health.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, dosage, frequency, purpose FROM intake")
    records = cursor.fetchall()
    conn.close()

    return records
