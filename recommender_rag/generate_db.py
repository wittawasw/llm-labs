import sqlite3

def create_db():
    conn = sqlite3.connect("./db/recommender_rag.db")
    cursor = conn.cursor()

    # Medications table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            commercial_name VARCHAR(64),
            dosage VARCHAR(32),
            price FLOAT,
            stock_quantity INTEGER,
            ingredients TEXT
        )
    """)

    # Supplements Knowledge Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS supplements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            benefits TEXT,
            price FLOAT,
            stock_quantity INTEGER
        )
    """)

    # Intake table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS intake (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            substance_name VARCHAR(64),
            dosage VARCHAR(16),
            frequency VARCHAR(16),
            purpose TEXT,
            medication_id INTEGER,
            intake_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (medication_id) REFERENCES medications(id)
        )
    """)

    sample_medications = [
        ("Vitamin C Soluble Tablet", "1000mg", 150.0, 50, "Vitamin C, Calcium, Vitamin D"),
        ("Omega-3 Fish Oil", "1000mg", 300.0, 20, "Omega-3, DHA, EPA")
    ]

    sample_supplements = [
        ("Vitamin C", "An essential vitamin for immunity.", "Boosts immune system, antioxidant.", 100.0, 30),
        ("Omega-3", "Essential fatty acids from fish oil.", "Supports heart health, brain function.", 250.0, 20)
    ]

    sample_intake = [
        ("Vitamin C", "500mg", "Daily", "Immune support", 1),
        ("Omega-3", "1000mg", "Daily", "Heart health", 2)
    ]

    for med in sample_medications:
        cursor.execute("INSERT INTO medications (commercial_name, dosage, price, stock_quantity, ingredients) VALUES (?, ?, ?, ?, ?)", med)

    for supp in sample_supplements:
        cursor.execute("INSERT INTO supplements (name, description, benefits, price, stock_quantity) VALUES (?, ?, ?, ?, ?)", supp)

    for intake in sample_intake:
        cursor.execute("INSERT INTO intake (substance_name, dosage, frequency, purpose, medication_id, intake_datetime) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", intake)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
    print("Database created with tables and sample data including price and stock quantity.")
