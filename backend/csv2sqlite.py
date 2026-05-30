import zipfile
import csv_to_sqlite

DB_FILE = "database.sqlite"

with zipfile.ZipFile("data/DDIDataset.zip", 'r') as zip_ref:
    zip_ref.extractall("data/")

options = csv_to_sqlite.CsvOptions(typing_style="full", encoding="windows-1250", delimiter=";")
input_files = ["data/DDIDataset.csv"]
csv_to_sqlite.write_csv(input_files, DB_FILE, options)