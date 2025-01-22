import firebase_admin
from firebase_admin import credentials, firestore
import csv

# Initialize Firebase Admin SDK
cred = credentials.Certificate('/Users/delaneyfisher/Documents/Mobile App Dev/budgetbasket-82776-firebase-adminsdk-s493t-4c3071fa27.json')
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# Open the CSV file and process each row
with open('items.csv', mode='r', newline='') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip header row
    
    for row in csv_reader:
        item = row[0]
        hannaford = float(row[1])
        shaws = float(row[2])
        price_chopper = float(row[3])
        trader_joes = float(row[4])

        # Define stores list
        stores_list = [
            {
                "name": "Hannaford",
                "price": hannaford,
                "temporaryPrice": False
            },
            {
                "name": "Shaw's",
                "price": shaws,
                "temporaryPrice": False
            },
            {
                "name": "Price Chopper",
                "price": price_chopper,
                "temporaryPrice": False
            },
            {
                "name": "Trader Joe's",
                "price": trader_joes,
                "temporaryPrice": False
            }
        ]

        # Define the item to be added to Firestore with an empty "image" field
        item_to_add = {
            "name": item,
            "stores": stores_list,
            "image": ""  # Add an empty string for the "image" field
        }

        # Add the item to Firestore
        try:
            db.collection('items').add(item_to_add)
        except Exception as e:
            print(f"Error adding item: {e}")
