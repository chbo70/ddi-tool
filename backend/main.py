from fastapi import FastAPI, Header, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
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
    conn.row_factory = sqlite3.Row  # gets results as dict
    return conn

def parse_percentage(value):
    return (
        float(str(value).replace(",", "."))
        if isinstance(value, str)
        else float(value or 0)
    )


@app.on_event("startup")
def startup_db():
    conn = get_db_connection()
    conn.close()
    print("Datenbank lauft ")


@app.get("/")
def read_root():
    return {"message": "DDI Tool by V3ctor2"}


@app.get("/api/patients")
def get_patients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return {"patients": patients}


@app.get("/api/prefetch/{patient_id}")
def prefetch_drugs(patient_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM patient_drugs WHERE patient_id = ?", (patient_id,)
    )  # gets all drugs for the patient from the database
    patient_drugs = cursor.fetchall()
    drug_list = [row["drug_name"] for row in patient_drugs]
    
    placeholders = ",".join(["?"] * len(drug_list))
    query = f"SELECT * FROM drugs WHERE drug1 IN ({placeholders}) OR drug2 IN ({placeholders})"  # collects all interactions for the provided drugs

    cursor.execute(query, drug_list + drug_list)
    interactions = cursor.fetchall()
    conn.close()

    BACKEND_CACHE[SESSION_ID] = {
        "interactions": interactions,
        "patient_drugs": [d.lower() for d in drug_list],
    }  # writes results into cache for a session
    return {"patient_drugs": patient_drugs}


@app.post("/api/interaction")
def get_drug_interaction(drug: str = Body(..., embed=True)):
    cache_data = BACKEND_CACHE.get(
        SESSION_ID
    )  # retrieves prefetched data for the session from cache

    if not cache_data:
        raise HTTPException(status_code=404, detail="Cache empty or session expired")

    prefetched_interactions = cache_data["interactions"]
    patient_drugs = cache_data["patient_drugs"]
    
    results = {}
    search_drug = drug.lower().strip()
    
    for row in prefetched_interactions:  # checks if the drug is part of the interaction in the prefetched data
        drug1_val = str(row["drug1"].lower())
        drug2_val = str(row["drug2"].lower())
        
        # search for both direct and reverse match
        if search_drug in drug1_val or search_drug in drug2_val:
            other_drug = drug2_val if search_drug in drug1_val else drug1_val
            is_prescribed  = any(prescribed_drug in other_drug or other_drug in prescribed_drug for prescribed_drug in patient_drugs)
            
            if is_prescribed:
                key = tuple(sorted([row["drug1"], row["drug2"]]))
                percentage = parse_percentage(row["percentage"])
                interaction = row["interaction"]

                if key not in results or percentage > parse_percentage(results[key]["percentage"]):
                    results[key] = {
                        "drug1": row["drug1"],
                        "drug2": row["drug2"],
                        "interaction": interaction,
                        "percentage": percentage,
                    }

    # del BACKEND_CACHE[SESSION_ID] # clears cache after use
    return {"interactions": list(results.values())}


class AddDrugRequest(BaseModel):
    drug_name: str
    has_interaction: bool = False
    interaction: Optional[str] = None

@app.post("/api/patients/{patient_id}/drugs")
def add_patient_drug(patient_id: int, drug_data: AddDrugRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO patient_drugs (patient_id, drug_name, has_interaction, interaction)
        VALUES (?, ?, ?, ?)
    """, (patient_id, drug_data.drug_name.strip(), drug_data.has_interaction, drug_data.interaction))

    cursor.execute("""
        UPDATE patients 
        SET drugCounter = drugCounter + 1 
        WHERE id = ?
    """, (patient_id,))

    conn.commit()
    conn.close()

    if SESSION_ID in BACKEND_CACHE:
        del BACKEND_CACHE[SESSION_ID]

    return {"status": "success"}