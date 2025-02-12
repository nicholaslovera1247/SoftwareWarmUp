"""Module that contains several methods for interacting 
with the Firebase database in various ways"""

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

def authentication():
    """Creats auth credits for the database, and retuns a pointer to the database"""

    cred = credentials.Certificate(r"./pokemon_db_certs.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

def delete_collection(auth):
    """Empties the database"""

    collection_ref = auth.collection("pokemon")
    docs = collection_ref.stream()
    for doc in docs:
        doc.reference.delete()

def add_document(document, auth):
    """Adds a given document into the "pokemon" collection in Firebase"""

    collection_name = "pokemon"
    document_id = document.get("id", auth.collection(collection_name).document().id)
    auth.collection(collection_name).document(document_id).set(document)

def query_database(key, op, value, auth):
    """Sends a query to the database, and returns the result"""

    collection_ref = auth.collection("pokemon")
    query_ref = collection_ref.where(filter=FieldFilter(key, op, value))
    docs = query_ref.get()
    return docs
