import os

# Bibliothèques standard
import csv
import logging
from pathlib import Path

# Bibliothèques tierces
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

# Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "medical_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "hospitalizations")

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Chemin du fichier CSV
CSV_FILE = Path(__file__).parent.parent / "data" / "healthcare_dataset.csv"

def build_document(row):
    return {
        "patient": {
            "name": row["Name"].title().strip(),
            "age": int(row["Age"]),
            "gender": row["Gender"],
            "bloodType": row["Blood Type"]
        },
        "hospitalization": {
            "admissionDate": row["Date of Admission"],
            "dischargeDate": row["Discharge Date"],
            "roomNumber": int(row["Room Number"]),
            "admissionType": row["Admission Type"]
        },
        "diagnosis": {
            "medicalCondition": row["Medical Condition"],
            "testResults": row["Test Results"]
        },
        "treatment": {
            "medication": row["Medication"]
        },
        "doctor": {
            "name": row["Doctor"].title().strip()
        },
        "hospital": {
            "name": row["Hospital"].strip()
        },
        "billing": {
            "insuranceProvider": row["Insurance Provider"],
            "billingAmount": float(row["Billing Amount"])
        }
    }

def connect_to_mongodb():
    try:
        client = MongoClient(MONGO_URI)
        client.admin.command("ping")
        
        logging.info("Connexion à MongoDB réussie.")

        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        return collection

    except ConnectionFailure:
        logging.error("Impossible de se connecter à MongoDB.")
        raise SystemExit(1)

def import_data(collection):
    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        count = 0

        for row in reader:
            document = build_document(row)

            try:
                collection.insert_one(document)

            except PyMongoError as e:
                logging.error(f"Erreur lors de l'insertion : {e}")

            count += 1

            if count % 100 == 0:
                logging.info(f"{count} documents importés...")

    logging.info(f"Migration terminée : {count} documents importés.")

def main():
    collection = connect_to_mongodb()
    import_data(collection)

if __name__ == "__main__":
    main()