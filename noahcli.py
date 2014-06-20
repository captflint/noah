import lzma
import pickle
import curses
from random import randint
from index import index
from doubleentries import doubleentries
with lzma.open('webster.txt.xz', 'rt') as infile:
    webster = infile.read()

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
            history.history.append(query)
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
        history.viewHistory()
        menu()
    else:
        menu()

def lookupmode():
    q = input('Enter a word to look up: ')
    while q != '?':
        definition = lookup(q)
        print(definition)
        q = input('Enter a word to look up: ')
    menu('?')

class History:
    def __init__(self):
        try:
            with open('historypickle', 'rb') as infile:
                self.history = pickle.load(infile)
        except FileNotFoundError:
            self.history = []
        self.positionList = []

    def writeToScreen(self, offset):
        height = screen.getmaxyx()[0]
        self.positionList = []
        if offset < 0:
            begin = 0
        else:
            begin = offset
        if begin + height > len(self.rlist):
            end = len(self.rlist)
        else:
            end = begin + height
        screen.clear()
        for item in self.rlist[begin:end]:
            screen.addstr(item)
            self.positionList.append((screen.getyx()[0], item))
            if screen.getyx()[0] != height -1:
                screen.addstr('\n')

    def viewHistory(self):
        self.rlist = []
        for word in reversed(self.history):
            self.rlist.append(word)
        offset = 0
        self.writeToScreen(offset)
        screen.move(0, 0)
        command = chr(screen.getch())
        position = 0
        while command not in 'qQ':
            if command in 'lL':
                for pair in self.positionList:
                    if position == pair[0]:
                        scrollythingy(lookup(pair[1]))
            elif command in 'wW':
                position -= 1
            elif command in 'sS':
                position += 1
            if position < 0:
                position = 0
                offset -= 1
                self.writeToScreen(offset)
            elif position >= screen.getmaxyx()[0]:
                position = screen.getmaxyx()[0] - 1
                offset += 1
                self.writeToScreen(offset)
            screen.move(position, 0)
            command = chr(screen.getch())

history = History()
menu()
