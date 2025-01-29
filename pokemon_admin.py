import firebase_admin
from firebase_admin import credentials, firestore
import json

cred = credentials.Certificate(r"path to json")
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# Delete existing collection
collection_ref = db.collection("pokemon")
docs = collection_ref.stream()
for doc in docs:
    doc.reference.delete()

# read json file
with open("pokemon.json", "r") as file:
    json_data = json.load(file)

try:
    if isinstance(json_data, list):
        collection_name = "pokemon" 
        for document in json_data:
            document_id = document.get("id", db.collection(collection_name).document().id)
            db.collection(collection_name).document(document_id).set(document)
            print(f"Document {document_id} written to {collection_name}.")
except Exception as e:
    print(f"An error occurred: {e}")
