import zipfile
import csv
import sqlite3

DB_FILE = "database.sqlite"

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
        interaction BOOLEAN DEFAULT 0,
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

with open('data/DDIDataset.csv','r', encoding='utf-8-sig') as fin:
    dr = csv.DictReader(fin, delimiter=';')
    print("Detected headers:", dr.fieldnames)
    to_db = [(i['Drug1'], i['Drug2'], i['Percentage'], i['Interaction']) for i in dr]

cursor.executemany("INSERT INTO drugs (drug1, drug2, percentage, interaction) VALUES (?, ?, ?, ?);", to_db)
conn.commit()

conn.close()