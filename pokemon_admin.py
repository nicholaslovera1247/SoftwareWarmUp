"""Module docstring (TODO)"""

import json
from pokemon_firebase import delete_collection, add_document, authentication

# authentication
auth = authentication()

# Delete existing collection
delete_collection(auth)

# Read json file
JSON_FILE = "pokeemon.json"
with open(JSON_FILE, "r", encoding='UTF-8') as file:
    json_data = json.load(file)

# Add documents to Firebase
try:
    if isinstance(json_data, list):
        for document in json_data:
            add_document(document, auth)
except FileNotFoundError as e:
    print(f"An error occurred: {e}")
