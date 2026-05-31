from fastapi import FastAPI, Header, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "database.sqlite"
BACKEND_CACHE = {}
SESSION_ID = 1

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row # gets results as dict
    return conn

@app.on_event("startup")
def startup_db():
    conn = get_db_connection()
    conn.close()
    print("Datenbank lauft ")


@app.get("/")
def read_root():
    return {"message": "DDI Tool by V3ctor2"}

@app.get("/patients")
def get_patients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return {"patients": patients}

@app.get("/prefetch/{patient_id}")
def prefetch_drugs(patient_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patient_drugs WHERE patient_id = ?", (patient_id,)) # gets all drugs for the patient from the database
    patient_drugs = cursor.fetchall()
    drug_list = [row["drug_name"] for row in patient_drugs]

    placeholders = ','.join(['?'] * len(drug_list))
    query = f"SELECT * FROM drugs WHERE drug1 IN ({placeholders}) OR drug2 IN ({placeholders})" # collects all interactions for the provided drugs

    cursor.execute(query, drug_list + drug_list)
    drugs = cursor.fetchall()
    conn.close()
    
    BACKEND_CACHE[SESSION_ID] = drugs # writes results into cache for a session
    return patient_drugs


@app.post("/interaction")
def get_drug_interaction(drug: str = Body(..., embed=True)):
    prefetched_data = BACKEND_CACHE.get(SESSION_ID) # retrieves prefetched data for the session from cache
    
    if not prefetched_data:
        raise HTTPException(status_code=404, detail="Cache empty or session expired")

    results = {}
    for row in prefetched_data: # checks if the drug is part of the interaction in the prefetched data
        if any(isinstance(cell, str) and drug in cell for cell in row):
            key = tuple(sorted([row["drug1"], row["drug2"]]))
            percentage = parse_percentage(row["percentage"])
            interaction = row["interaction"]

            if key not in results or percentage > parse_percentage(results[key]["percentage"]):
                results[key] = { "drug1": row["drug1"], "drug2": row["drug2"], "interaction": interaction, "percentage": percentage}

    del BACKEND_CACHE[SESSION_ID] # clears cache after use
    return {"results": list(results.values())}


def parse_percentage(value):
    return float(str(value).replace(',', '.')) if isinstance(value, str) else float(value or 0)