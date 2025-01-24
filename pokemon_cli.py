def take_input():
    quit = False;

    while not quit:
        print('>', end ='')
        query = input().lower().strip().split(' ')

        if query[0] == 'quit':
            quit = True;



take_input()
print("Goodbye!")
