# scripts/2_export_firestore.py
import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

# Initialize Firebase
cred = credentials.Certificate(r"C:\Users\DELL\Desktop\recipe-pipeline\serviceAccount.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Make folder
os.makedirs("exports", exist_ok=True)

def export_collection_to_json(col_name):
    docs = db.collection(col_name).stream()
    data = []

    for doc in docs:
        d = doc.to_dict()
        d["document_id"] = doc.id     # include Firestore doc ID
        data.append(d)

    filepath = f"exports/{col_name}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"Exported {col_name} → {filepath}")

# Export all required collections
export_collection_to_json("recipes")
export_collection_to_json("users")
export_collection_to_json("interactions")

print("\nFirestore RAW export complete! JSON files stored in /exports/")
