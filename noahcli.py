import lzma
from random import randint
from index import index
with lzma.open('webster.txt.xz', 'rt') as infile:
    webster = infile.read()

def lookup(query):
    query = query.upper()
    for current in range(0, len(index)):
        if query == index[current][1]:
            return(webster[index[current][0]:index[current + 1][0]])
    return('Word not found')

def randomword():
    r = randint(0, len(index))
    return(webster[index[r][0]:index[r + 1][0]])

def menu(command):
    if command == '?':
        print('L - Look up a word')
        print('R - Look up a random word')
        print('Q - Quit the program')
        print('? - Display this menu')
        menu(input('Enter a command: '))
    elif command in 'lL':
        lookupmode()
    elif command in 'rR':
        print(randomword())
        menu('?')
    elif command in 'qQ':
        quit()
    else:
        menu('?')

def lookupmode():
    q = input('Enter a word to look up: ')
    while q != '?':
        definition = lookup(q)
        print(definition)
        q = input('Enter a word to look up: ')
    menu('?')

print('Enter "?" for a menu')
lookupmode()
