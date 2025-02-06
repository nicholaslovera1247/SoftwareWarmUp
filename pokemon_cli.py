from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import credentials, firestore
import firebase_admin
from PokemonClass import Pokemon


cred = credentials.Certificate(r"./pokemon_db_certs.json")
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

KEYS = ['index', 'hp', 'stage', 'name', 'type', 'quit', 'help']
OPS = ['of', '==', '!=', '<=', '>=', '<', '>']
TYPES = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 
        'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'fairy']

def query_firebase(query):
    collection = db.collection('pokemon')

    all_pokemon = []
    merge_type = ''

    for subquery in query:
        # check if subquery is of format [key, operator, value], if it is not in this format then it is invalid
        if subquery in ['and', 'or']:
            merge_type = subquery
        else:
            new_pokemon = []

            key, op, value = subquery
            query_ref = collection.where(filter=FieldFilter(key, op, value))
            docs = query_ref.get()
            for doc in docs:
                new_pokemon.append(Pokemon.from_dict(doc.to_dict()))

            if all_pokemon == []:
                all_pokemon = new_pokemon

            if merge_type == 'and':
                all_pokemon = merge_and(all_pokemon, new_pokemon)
            if merge_type == 'or':
                all_pokemon = merge_or(all_pokemon, new_pokemon)

            merge_type == ''
    
    result = docs

    return all_pokemon
    
def take_input():
    while True:
        valid_query = True

        print('> ', end ='')
        input_str = input().lower().strip().split(' ')

        if input_str[0] == 'quit':
            break

        if input_str[0] == 'help':
            help()

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

        if valid_query:
            query_output = query_firebase(query)

            for pokemon in query_output:
                print(pokemon)

        print()

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

def merge_and(list1,list2):
    # Compare unique IDs of each document in the Google firestore
    set1 = {doc.id for doc in list1}
    set2 = {doc.id for doc in list2}
    # Using pythons intersection method, get the common documents in both lists
    common_ids = set1.intersection(set2)
    # Iterate through list 1 (or 2), if the doc.id in this list is in common_ids, add it to our list of
    # common documents from both list
    rtnlist = []
    for doc in list1:
        if doc.id in common_ids:
            rtnlist.append(doc)
    return rtnlist

def merge_or(list1,list2):
    # Create a set to avoid duplicates
    seen = set()
    # Create a list that merges list 1 and list 2
    merged = []
    # Iterate through list 1 and list 2, if the doc is not already in seen, append it to our merged list
    for doc in list1 + list2:
        if doc.id not in seen:
            seen.add(doc.id)
            merged.append(doc)
    return merged

def help():
    print("Keywords: Index, name, type, HP, stage, help, quit \n"
          "Operators: ==, !=, <=, >=, <, >, <, >, and, of\n"
          "--------------------------------------------------\n"
          "Index (int):  ==, !=, <=, >=, <, >, of\n"
          "Name (str): ==, of\n"
          "Type (str): ==, !=, of (normal, fire, water, electric, grass, ice, fighting, \n"
          "poison, ground, flying, psychic, bug, rock, ghost, dragon, dark, steel, fairy)\n"
          "HP (int): ==, !=, <=, >=, <, >, of\n"
          "Stage (int): ==, !=, <=, >=, <, >, of (1, 2, 3)\n"
          "quit: Close program\n"
          "help: List commands\n"
          "--------------------------------------------------\n"
          "“Of” operator: [keyword] of [index/name]:\n"
          "Returns the specified column of the given pokemon\n"
          "Must use either the name or index of a pokemon to get a result\n"
          "--------------------------------------------------\n"
          "Example queries:\n"
          "> name == pikachu:\n"
          "> type == dragon\n"
          "> type == grass or type == fire\n"
          "> index <= 1 and HP > 100\n"
          "> name of 4")
take_input()
print("Goodbye!")
