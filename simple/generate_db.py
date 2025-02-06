import sqlite3

def create_db():
    conn = sqlite3.connect("./db/example.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receipts (
            receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name VARCHAR(16),
            price FLOAT,
            tip FLOAT
        )
    """)
    sample_data = [
        ("Alice", 120.0, 18.0),
        ("Bob", 75.0, 9.0),
        ("Charlie", 200.0, 25.0),
        ("Diana", 50.0, 5.0)
    ]
    for data in sample_data:
        cursor.execute("INSERT INTO receipts (customer_name, price, tip) VALUES (?, ?, ?)", data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
    print("Database 'example.db' with table 'receipts' created.")
