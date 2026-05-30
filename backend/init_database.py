import zipfile
import csv_to_sqlite
import sqlite3

DB_FILE = "database.sqlite"

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
conn.close()

with zipfile.ZipFile("data/DDIDataset.zip", 'r') as zip_ref:
    zip_ref.extractall("data/")

options = csv_to_sqlite.CsvOptions(typing_style="full", encoding="windows-1250", delimiter=";")
input_files = ["data/DDIDataset.csv"]
csv_to_sqlite.write_csv(input_files, DB_FILE, options)