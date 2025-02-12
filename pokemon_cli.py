"""Module that runs a CLI program which asks the user for an input query based around Pokemon, 
and prints the output of their query"""

import pyparsing as pp
from pokemon_firebase import authentication, query_database
from pokemon_class import Pokemon

# Define terms for creating pyparsing queries
all_keys = pp.one_of('name type index hp stage') # All keywords
int_keys = pp.one_of('index hp stage') # Keywords that take ints
int_ops = pp.one_of('== != <= >= < >') # Operators used for keywords that take ints
str_ops = pp.one_of('== !=') # Operators used for keywords that take strs
types = pp.one_of(
    'normal fire water electric grass ice fighting poison \
    ground flying psychic bug rock ghost dragon dark fairy'
    ) # Allowed types to query for
logic = pp.one_of('and or') # Allowed forms of logic to combine multiple queries

# Define regex to parse over
basic_query_format = (
    # Handles queries with int arguments
    (int_keys + int_ops + pp.Word(pp.nums).set_parse_action(lambda tokens: int(tokens[0]))) |
    # Handles 'name' queries
    ('name' + str_ops + pp.Word(pp.printables)) |
    # Handles 'type' queries
    ('type' + str_ops + types)
    # Nest queries into separate lists for easier parsing of complex queries
    ).set_parse_action(lambda tokens: [tokens])

# Handles 'of' queries
of_query_format = (
    (all_keys + 'of' + (
        pp.Word(pp.nums).set_parse_action(lambda tokens: int(tokens[0])) |
        pp.Word(pp.printables)))
    ).set_parse_action(lambda tokens: [tokens])

# Complex queries, allows for using 'and' or 'or' to
# add multiple forms of logic, as well as 'of' queries
query_format = (basic_query_format + (logic + basic_query_format)[0,]) | of_query_format

auth = authentication()

def query_firebase(query):
    """Takes a formatted query from take_input(), 
    sends it to the Firebase database, and returns the result"""

    all_pokemon = []
    merge_type = ''

    for subquery in query:
        # check if subquery is of format [key, operator, value],
        # if it is not in this format then it is invalid
        if subquery in ['and', 'or']:
            merge_type = subquery
        else:
            key, op, value = subquery

            if op == 'of':
                if isinstance(value, int):
                    docs = query_database('index', '==', value, auth)
                else:
                    docs = query_database('name', '==', value, auth)
                for doc in docs:
                    all_pokemon = Pokemon.from_dict(doc.to_dict())
            else:
                new_pokemon = []
                docs = query_database(key, op, value, auth)
                for doc in docs:
                    new_pokemon.append(Pokemon.from_dict(doc.to_dict()))

                if not all_pokemon:
                    all_pokemon = new_pokemon

                if merge_type == 'and':
                    all_pokemon = merge_and(all_pokemon, new_pokemon)
                if merge_type == 'or':
                    all_pokemon = merge_or(all_pokemon, new_pokemon)

                merge_type = ''
    return all_pokemon

def merge_and(list1,list2):
    """Takes 2 lists of Pokemon, and returns a list containing the intersection of those lists"""

    # Compare unique IDs of each document in the Google firestore
    set1 = {doc.index for doc in list1}
    set2 = {doc.index for doc in list2}
    # Using pythons intersection method, get the common documents in both lists
    common_ids = set1.intersection(set2)
    # Iterate through list 1 (or 2), if the doc.id in this list is in common_ids,
    # add it to our list of common documents from both list
    rtnlist = []
    for doc in list1:
        if doc.index in common_ids:
            rtnlist.append(doc)
    return rtnlist

def merge_or(list1,list2):
    """Takes 2 lists of Pokemon, and returns a list containing the union of those lists"""

    # Create a set to avoid duplicates
    seen = set()
    # Create a list that merges list 1 and list 2
    merged = []
    # Iterate through list 1 and list 2, if the doc is not already in seen,
    # append it to our merged list
    for doc in list1 + list2:
        if doc.index not in seen:
            seen.add(doc.index)
            merged.append(doc)
    return merged

def take_input():
    """Main body of the program, loops until exited and asks the user for input, 
    before validating the format and calling query_firebase() if appropriate"""

    print("Welcome to the Pokemon CLI! Enter 'help' for more info on query format.")
    while True:
        valid_query = True
        query = []

        print('\n> ', end='')
        input_str = input().lower().strip()
        print()

        # Handle special cases for input that do not match regular query structure
        if input_str == 'quit':
            break

        if input_str == 'help':
            help_query()
            continue

        # Attempt to parse input, print error message if it does not match query structure
        try:
            query = query_format.parse_string(input_str, parse_all=True)
        except pp.ParseException as ex:
            print(ex)
            valid_query = False

        # If query was properly parsed, send it to firebase and print the result
        if valid_query:
            query_output = query_firebase(query)
            if query_output == []:
                print("No results found.")
            elif query[0][1] == 'of':
                field = query[0][0]
                print(getattr(query_output, field))
            else:
                for pokemon in query_output:
                    print(pokemon)
        else:
            print('Use \'help\' for more info')

def help_query():
    """Prints the documentation for the query language, as well as some example queries"""

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
          "May not create compound queries with \'and\' or \'or\'\n"
          "--------------------------------------------------\n"
          "Example queries:\n"
          "> name == pikachu:\n"
          "> type == dragon\n"
          "> type == grass or type == fire\n"
          "> index <= 1 and HP > 100\n"
          "> name of 4")

take_input()
print("Goodbye!")
