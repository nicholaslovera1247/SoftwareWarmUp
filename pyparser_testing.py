import pyparsing as pp

int_keys = pp.one_of('index hp stage')
int_ops = pp.one_of('of == != <= >= < >')
str_ops = pp.one_of('of == !=')
types = pp.one_of('normal fire water electric grass ice fighting poison ' + 
                  'ground flying psychic bug rock ghost dragon dark fairy')
logic = pp.one_of('and or')


query_format = (int_keys + int_ops + pp.Word(pp.nums)) | ('name' + str_ops + pp.Word(pp.printables)) | ('type' + str_ops + types)
complex_query_format = query_format + (logic + query_format)[0,]

def take_input():
    while True:
        valid_query = True
        input_list = ''

        print('\n>', end='')
        input_str = input().lower()

        if input_str == 'quit':
            break

        if input_str == 'help':
            #help()
            continue
        
        try:
            input_list = complex_query_format.parse_string(input_str, parse_all=True)
        except pp.ParseException as ex:
            print(ex)
            valid_query = False

        query = []
        subquery = []
        for word in input_list:
            if word not in ['and', 'or']:
                subquery.append(word)
            else:
                query.append(subquery)
                subquery = []
                query.append(word)
        query.append(subquery)

        if valid_query:
            print(query)

take_input()