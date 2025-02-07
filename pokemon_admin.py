from pokemon_firebase import delete_collection, add_document, authentication
import json

# authentication
auth = authentication()

# Delete existing collection
delete_collection(auth)

# Read json file
json_file = "pokemon.json"
with open(json_file, "r") as file:
        json_data = json.load(file)

# Add documents to Firebase
try:
    if isinstance(json_data, list):
        for document in json_data:
            add_document(document, auth)
except Exception as e:
        print(f"An error occurred: {e}")