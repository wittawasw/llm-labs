import sqlite3

def create_db():
    conn = sqlite3.connect("./db/health.db")
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
    """
    )

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
    """
    )

    sample_medications = [
        ("Vitamin C Soluble Tablet", "1000mg", 150.0, 50, "Vitamin C, Calcium, Vitamin D"),
        ("Omega-3 Fish Oil", "1000mg", 300.0, 20, "Omega-3, DHA, EPA"),
        ("Magnesium Citrate", "200mg", 180.0, 40, "Magnesium Citrate"),
        ("Zinc Gluconate", "30mg", 120.0, 60, "Zinc Gluconate"),
        ("Iron Tablets", "65mg", 250.0, 30, "Iron, Vitamin C"),
        ("B-Complex", "500mg", 200.0, 25, "Vitamin B1, B2, B6, B12"),
        ("Calcium & D3", "600mg", 280.0, 45, "Calcium, Vitamin D3"),
        ("Multivitamin Daily", "1 Tablet", 350.0, 100, "Vitamin A, B, C, D, E, Zinc, Iron"),
        ("Probiotic Capsules", "10 billion CFU", 400.0, 30, "Lactobacillus, Bifidobacterium"),
        ("CoQ10 Softgels", "100mg", 500.0, 20, "Coenzyme Q10"),
        ("Turmeric Curcumin", "500mg", 270.0, 50, "Curcumin, Black Pepper"),
        ("Collagen Peptides", "10g", 600.0, 40, "Collagen, Hyaluronic Acid"),
        ("Green Tea Extract", "500mg", 320.0, 30, "Green Tea, EGCG"),
        ("Ginkgo Biloba", "120mg", 200.0, 25, "Ginkgo Biloba Extract"),
        ("Ashwagandha Capsules", "600mg", 350.0, 30, "Ashwagandha Root"),
        ("Melatonin Tablets", "3mg", 180.0, 50, "Melatonin"),
        ("L-Theanine", "200mg", 250.0, 40, "L-Theanine"),
        ("Resveratrol", "250mg", 420.0, 20, "Resveratrol"),
        ("Biotin Hair Growth", "10,000mcg", 280.0, 45, "Biotin, Zinc, Folic Acid"),
        ("Chondroitin & Glucosamine", "1500mg", 500.0, 30, "Chondroitin, Glucosamine, MSM")
    ]

    sample_intake = [
        ("Vitamin C", "500mg", "Daily", "Immune support", 1),
        ("Omega-3", "1000mg", "Daily", "Heart health", 2),
        ("Magnesium", "200mg", "Nightly", "Muscle recovery", 3),
        ("Zinc", "30mg", "Every other day", "Wound healing", 4),
        ("Iron", "65mg", "Weekly", "Anemia prevention", 5)
    ]

    for med in sample_medications:
        cursor.execute("INSERT INTO medications (commercial_name, dosage, price, stock_quantity, ingredients) VALUES (?, ?, ?, ?, ?)", med)

    for intake in sample_intake:
        cursor.execute("INSERT INTO intake (substance_name, dosage, frequency, purpose, medication_id, intake_datetime) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", intake)


    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
    print("Database 'health.db' with tables 'medications' and 'intake' created.")
