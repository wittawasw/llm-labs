import sqlite3

def fetch_intake():
    conn = sqlite3.connect("./db/recommender_rag.db")
    cursor = conn.cursor()
    cursor.execute("SELECT substance_name, dosage, frequency, purpose, medication_id FROM intake")
    records = cursor.fetchall()
    conn.close()
    return records
