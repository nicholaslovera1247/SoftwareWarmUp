from pokemon_admin import db

KEYS = ['index', 'name', 'type', 'hp', 'stage', 'quit', 'help']
OPS = ['of', '==', '!=', '<=', '>=', '<', '>']
TYPES = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 
        'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'fairy']

def query_firebase(query):
    collection = db.collection('pokemon')
    firebase_query = collection

    for subquery in query:
        # check if subquery is of format [key, operator, value], if it is not in this format then it is invalid
        if len(subquery) == 3:
            key, op, value = subquery
            if key in KEYS and op in OPS:
                firebase_query = firebase_query.where(key, op, value)
    
    result = firebase_query.get()
    
def take_input():
    while True:
        print('> ', end ='')
        input_str = input().lower().strip().split(' ')

        if input_str[0] == 'quit':
            break

        query = []
        subquery = []
        for word in input_str:
            if word not in {'and', 'or'}:
                subquery.append(word)
            else:
                query.append(subquery)
                subquery = []
        query.append(subquery)

        print(query)

take_input()
print("Goodbye!")
