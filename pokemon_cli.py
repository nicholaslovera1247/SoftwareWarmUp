from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import credentials, firestore
import firebase_admin

cred = credentials.Certificate(r"../pokemon_db_certs.json")
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

KEYS = ['index', 'hp', 'stage', 'name', 'type', 'quit', 'help']
OPS = ['of', '==', '!=', '<=', '>=', '<', '>']
TYPES = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 
        'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'fairy']

def query_firebase(query):
    collection = db.collection('pokemon')

    for subquery in query:
        # check if subquery is of format [key, operator, value], if it is not in this format then it is invalid
        if len(subquery) == 3:
            key, op, value = subquery
            if key in KEYS and op in OPS:
                query_ref = collection.where(filter=FieldFilter(key, op, value))
                docs = query_ref.get()
                for doc in docs:
                    print(doc.to_dict())
    
    result = docs
    
def take_input():
    while True:
        valid_query = True

        print('> ', end ='')
        input_str = input().lower().strip().split(' ')

        if input_str[0] == 'quit':
            break
        
        if input_str == ['']:
            input_str = []

        query = []
        subquery = []
        for word in input_str:
            if word not in ['and', 'or']:
                subquery.append(word)
            else:
                query.append(subquery)
                subquery = []
                query.append(word)
        query.append(subquery)

        valid_query = validate_input(query)

        print(query, valid_query)

def validate_input(query):
    valid_query = True

    for subquery in query:
        if subquery in ['and', 'or']:
            continue
        # checks that each subquery has the correct length
        elif len(subquery) != 3:
            valid_query = False
            print(f'Expected 3 arguments ([keyword] [operator] [value]), found {len(subquery)} ({" ".join(map(str, subquery))})')
            continue

        key, op, val = subquery

        # checks that the given key value is a valid keyword
        if key not in KEYS:
            valid_query = False
            print(f'Keyword \'{key}\' not recognized')
        
        # checks that index, hp, and stage all get ints
        if key in KEYS[:3] and op != OPS[0]: 
            try:
                subquery[2] = int(val)
            except:
                valid_query = False
                print(f'Keyword \'{key}\' requires an int, found \'{val}\'')

        # checks that name and type are only used with 'of' or '=='
        if key in KEYS[3:5] and op != OPS[0]: 
            if op not in OPS[:2]:
                valid_query = False
                print(f'Keyword \'{key}\' requires either \'of\' or \'==\' operators, found \'{op}\'')

        # checks that type is always passed a valid type
        if key == KEYS[4] and op != OPS[0]:
            if val not in TYPES:
                valid_query = False
                print(f'Keyword \'{key}\' requires a valid type (see \'help\'), found \'{val}\'')

        # checks that the given op value is a valid operator
        if op not in OPS:
            valid_query = False
            print(f'Operator \'{op}\' not recognized')

        # if the 'of' operator is passed, converts val to an int if it is numeric
        if op == OPS[0]:
            try:
                subquery[2] = int(val)
            except:
                subquery[2] = val

    return valid_query

take_input()
print("Goodbye!")
