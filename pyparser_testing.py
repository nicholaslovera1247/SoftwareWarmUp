import pyparsing as pp

all_keys = pp.one_of('name type index hp stage')
int_keys = pp.one_of('index hp stage')
int_ops = pp.one_of('of == != <= >= < >')
str_ops = pp.one_of('of == !=')
types = pp.one_of('normal fire water electric grass ice fighting poison ' + 
                  'ground flying psychic bug rock ghost dragon dark fairy')
logic = pp.one_of('and or')


# Define regex to parse over
query_format = ((int_keys + int_ops + pp.Word(pp.nums).set_parse_action(lambda tokens: int(tokens[0]))) | 
                ('name' + str_ops + pp.Word(pp.printables)) | 
                ('type' + str_ops + types)).set_parse_action(lambda tokens: [tokens])
of_query_format = (
    (all_keys + 'of' + (pp.Word(pp.nums).set_parse_action(lambda tokens: int(tokens[0])) | pp.Word(pp.printables)))
    ).set_parse_action(lambda tokens: [tokens])

complex_query_format = query_format + (logic + query_format)[0,]

def take_input():
    while True:
        valid_query = True
        query = []

        print('\n>', end='')
        input_str = input().lower()
        print()

        # Handle special cases for input that to not match regular query structure
        if input_str == 'quit':
            break

        if input_str == 'help':
            help()
            continue
        
        # Attempt to parse input, print error message if it does not match query structure
        try:
            query = complex_query_format.parse_string(input_str, parse_all=True)
        except pp.ParseException as ex:
            print(ex)
            print('Use \'help\' for more info')
            valid_query = False

        if valid_query:
            print(query)

take_input()