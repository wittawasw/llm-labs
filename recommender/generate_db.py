import sqlite3

def create_db():
    conn = sqlite3.connect("./db/health.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS intake (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(32),
            dosage VARCHAR(16),
            frequency VARCHAR(16),
            purpose TEXT
        )
    """
    )

    sample_data = [
        ("Vitamin C", "500mg", "Daily", "Immune support"),
        ("Omega-3", "1000mg", "Daily", "Heart health"),
        ("Magnesium", "200mg", "Nightly", "Muscle recovery"),
        ("Zinc", "30mg", "Every other day", "Wound healing"),
    ]

    for data in sample_data:
        cursor.execute("INSERT INTO intake (name, dosage, frequency, purpose) VALUES (?, ?, ?, ?)", data)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
    print("Database 'health.db' with table 'intake' created.")
