import lzma
import pickle
from random import randint
from index import index
with lzma.open('webster.txt.xz', 'rt') as infile:
    webster = infile.read()
try:
    with open('historypickle', 'rb') as infile:
        history = pickle.load(infile)
except FileNotFoundError:
    history = []

def lookup(query):
    query = query.upper()
    history.append(query)
    for current in range(0, len(index)):
        if query == index[current][1]:
            return(webster[index[current][0]:index[current + 1][0]])
    return('Word not found')

def randomword():
    r = randint(0, len(index))
    history.append(index[r][1])
    return(webster[index[r][0]:index[r + 1][0]])

def menu(command):
    global history
    if command == '?':
        print('L - Look up a word')
        print('R - Look up a random word')
        print('H - View look up history')
        print('C - Clear look up history')
        print('Q - Quit the program')
        print('? - Display this menu')
        menu(input('Enter a command: '))
    elif command in 'lL':
        lookupmode()
    elif command in 'rR':
        print(randomword())
        menu('?')
    elif command in 'hH':
        viewhistory()
        menu('?')
    elif command in 'cC':
        history = []
        print('History cleared')
        menu('?')
    elif command in 'qQ':
        with open('historypickle', 'wb') as outfile:
            pickle.dump(history, outfile)
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

def viewhistory():
    global history
    displayed = 15
    reverseorderindex = -1
    while displayed > 0:
        if reverseorderindex * -1 > len(history):
            break
        else:
            print(reverseorderindex * -1, '\t' + history[reverseorderindex])
            reverseorderindex -= 1
            displayed -= 1
        if displayed == 0:
            c = input('"M" for more history, anything else to continue')
            if c in 'mM' and len(c) > 0:
                displayed = 15
    c = input('Look up number or go to menu')
    cisnumber = True
    for char in c:
        if char in '1234567890':
            continue
        else:
            cisnumber = False
            break
    if len(c) > 0 and cisnumber and 0 <= int(c) <= len(history):
        c = int(c)
        print(lookup(history[c * -1]))
        lookupmode()
    else:
        menu('?')

print('Enter "?" for a menu')
lookupmode()
