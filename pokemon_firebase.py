import firebase_admin 
from firebase_admin import credentials, firestore

def authentication():
    cred = credentials.Certificate(r"C:\Users\benth\OneDrive\Desktop\pokemon-authentication\pokemon-b8c62-firebase-adminsdk-fbsvc-9fe3b49643.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

def delete_collection(auth):
    collection_ref = auth.collection("pokemon")
    docs = collection_ref.stream()
    for doc in docs:
        doc.reference.delete()

def add_document(document, auth):
    collection_name = "pokemon"
    document_id = document.get("id", auth.collection(collection_name).document().id)
    auth.collection(collection_name).document(document_id).set(document)