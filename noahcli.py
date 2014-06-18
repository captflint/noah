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
        if chr(command) in 'Ww':
            if offset > 0:
                offset -= 1
        elif chr(command) in 'Ss':
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
    screen.addstr("'Q' to quit\n")
    screen.addstr("'R' to look up a random word\n")
    screen.addstr("'H' to look at history\n")
    screen.addstr("Use 'W', 'A', 'S', and 'D' to navigate")
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
    elif chr(command) in 'hH':
        scrollythingy(lookup(viewhistory()))
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
    displayed = 0
    reverseorderindex = -1
    height = screen.getmaxyx()[0]
    remember = 0
    while remember == 0:
        screen.clear()
        while displayed != height:
            screen.addstr(history[reverseorderindex])
            displayed += 1
            reverseorderindex -= 1
            if displayed != height:
                screen.addstr('\n')
            if reverseorderindex * -1 == len(history):
                break
        position = 0
        screen.move(position, 0)
        while position < height and -1 < position:
            screen.move(position, 0)
            command = chr(screen.getch())
            if command in 'wW':
                position -= 1
            elif command in 'sS':
                position += 1
            elif command in 'lL':
                remember = history[reverseorderindex + (height - screen.getyx()[0])]
                return(remember)
        if position == height:
            reverseorderindex -= height - 3
            if reverseorderindex * -1 >= len(history) + height:
                reverseorderindex = -1
        elif position == -1:
            reverseorderindex += height - 3
            if reverseorderindex >= 0:
                reverseorderindex = -1
        displayed = 0

menu()
