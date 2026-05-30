from fastapi import FastAPI
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

@app.on_event("startup")
def startup_db():
    conn = sqlite3.connect(DB_FILE)
    conn.close()
    print("Datenbank lauft ")

@app.get("/")
def read_root():
    return {"message": "DDI Tool by V3ctor2"}