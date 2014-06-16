import lzma
import pickle
import curses
from random import randint
from index import index
from doubleentries import doubleentries
with lzma.open('webster.txt.xz', 'rt') as infile:
    webster = infile.read()
try:
    with open('historypickle', 'rb') as infile:
        history = pickle.load(infile)
except FileNotFoundError:
    history = []

# initialize terminal screen
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
screen.refresh()

def scrollythingy(shitTonOfText):
    screen.clear()
    height = screen.getmaxyx()[0]
    command = 0
    offset = 0
    screen.scrollok(True)
    while chr(command) not in 'Qq':
        screen.clear()
        dispStr = ""
        lineCounter = 0
        for char in shitTonOfText:
            if char == "\n":
                lineCounter += 1
            if lineCounter >= offset and lineCounter < offset + height:
                dispStr += char
        screen.addstr(dispStr)
        command = screen.getch()
        if command == 259: #Up arrow key
            if offset > 0:
                offset -= 1
        elif command == 258: #Down arrow key
            offset += 1
        elif chr(command) in 'lL':
            screen.addstr(screen.getmaxyx()[0] - 1, 0, 'Look up word: ')
            curses.echo()
            userInput = bytes.decode(screen.getstr(), 'utf-8')
            curses.noecho()
            scrollythingy(lookup(userInput))
            menu()

def lookup(query):
    query = query.upper()
    for current in range(0, len(index)):
        if query == index[current][1]:
            history.append(query)
            return(webster[index[current][0]:index[current + 1][0]])
    for tup in doubleentries:
        for word in tup[1]:
            if query == word:
                return(lookup(tup[0]))
    return('Word not found')

def randomword():
    r = randint(0, len(index))
    return(lookup(index[r][1]))

def menu():
    screen.clear()
    screen.addstr("'L' to look up a word\n")
    screen.addstr("'Q' to quit")
    command = screen.getch()
    if chr(command) in 'lL':
        screen.addstr(screen.getmaxyx()[0] - 1, 0, 'Look up word: ')
        curses.echo()
        userInput = bytes.decode(screen.getstr(), 'utf-8')
        curses.noecho()
        scrollythingy(lookup(userInput))
        menu()
    elif chr(command) in 'qQ':
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()
        quit()
    else:
        menu()

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

menu()
