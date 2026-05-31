import zipfile
import csv
import sqlite3

DB_FILE = "database.sqlite"

def parse_percentage(val):
    if not val:
        return 0.0
    if isinstance(val, str):
        val = val.replace(',', '.')
    try:
        return float(val)
    except ValueError:
        return 0.0

with zipfile.ZipFile("data/DDIDataset.zip", 'r') as zip_ref:
    zip_ref.extractall("data/")

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        dob TEXT NOT NULL,
        drugCounter INTEGER DEFAULT 0
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS patient_drugs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        drug_name TEXT NOT NULL,
        is_interaction BOOLEAN DEFAULT 0,
        interaction TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS drugs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        drug1 TEXT NOT NULL,
        drug2 TEXT NOT NULL,
        percentage REAL,
        interaction TEXT
    )
""")

cursor.execute("SELECT COUNT(*) FROM drugs")

if cursor.fetchone()[0] == 0:
    with open('data/DDIDataset.csv','r', encoding='utf-8-sig') as fin:
        dr = csv.DictReader(fin, delimiter=';')
        print("Detected headers:", dr.fieldnames)
        to_db = [(i['Drug1'], i['Drug2'], parse_percentage(i['Percentage']), i['Interaction']) for i in dr]

    cursor.executemany("INSERT INTO drugs (drug1, drug2, percentage, interaction) VALUES (?, ?, ?, ?);", to_db)

cursor.execute("SELECT COUNT(*) FROM patients")

if cursor.fetchone()[0] == 0:
    patients_data = [
        ("Max Mustermann", "12.04.1985", 5),
        ("Erika Musterfrau", "05.11.1992", 4),
        ("Johannes Schmidt", "23.08.1964", 5),
        ("Anna Weber", "17.02.1978", 4)
    ]
    cursor.executemany(
        "INSERT INTO patients (name, dob, drugCounter) VALUES (?, ?, ?)", 
        patients_data
    )

    patient_drugs_data = [
        (1, "Aciclovir", 0, None),
        (1, "Amlodipine", 1, "aseptic necrosis bone"),
        (1, "Ofloxacin", 0, None),
        (1, "Aripiprazole", 0, None),
        (1, "Metformin", 0, None),
        
        (2, "Ibuprofen", 0, None),
        (2, "Lansoprazole", 0, "portal vein thrombosis"),
        (2, "Paracetamol", 0, None),
        (2, "Amoxapine", 0, None),
        
        (3, "Metoclopramide", 0, None),
        (3, "Fexofenadin", 0, None),
        (3, "Aspirin", 0, None),
        (3, "Warfarin", 0, None),
        (3, "Cetirizine", 0, None),
        
        (4, "Nitroglycerin", 0, None),
        (4, "Terazosin", 0, "balance disorder"),
        (4, "Clopidogrel", 0, None),
        (4, "Metoprolol", 0, "Embolism pulmonary")
    ]
    cursor.executemany(
        "INSERT INTO patient_drugs (patient_id, drug_name, is_interaction, interaction) VALUES (?, ?, ?, ?)", 
        patient_drugs_data
    )

conn.commit()
conn.close()