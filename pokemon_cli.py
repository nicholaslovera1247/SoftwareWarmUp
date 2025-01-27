KEYS = ['index', 'name', 'type', 'hp', 'stage', 'quit', 'help']
OPS = ['of', '==', '!=', '<=', '>=', '<', '>']
TYPES = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 
        'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'fairy']

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
                query.append(word)
        query.append(subquery)

        print(query)

take_input()
print("Goodbye!")
