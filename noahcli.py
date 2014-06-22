import lzma
import pickle
import curses
import random
import enchant
from index import index
from doubleentries import doubleentries
with lzma.open('webster.txt.xz', 'rt') as infile:
    webster = infile.read()
wordlist = enchant.request_pwl_dict('wordlist.txt')

# initialize terminal screen
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
screen.refresh()

def display(textchunk):
    screen.clear()
    height = screen.getmaxyx()[0]
    command = 0
    offset = 0
    screen.scrollok(True)
    while chr(command) not in 'Qq':
        screen.clear()
        dispStr = ""
        lineCounter = 0
        for char in textchunk:
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
            screen.clear()
            screen.addstr(screen.getmaxyx()[0] - 1, 0, 'Look up word: ')
            curses.echo()
            userInput = bytes.decode(screen.getstr(), 'utf-8')
            curses.noecho()
            display(lookup(userInput))
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
    spellcheck = Spellcheck(query)
    spellcheck.view()

def menu():
    screen.clear()
    screen.addstr("'L' to look up a word\n")
    screen.addstr("'Q' to quit\n")
    screen.addstr("'R' to look up a random word\n")
    screen.addstr("'H' to look at history\n")
    screen.addstr("Use 'W' and 'A' to navigate")
    command = screen.getch()
    if chr(command) in 'lL':
        screen.addstr(screen.getmaxyx()[0] - 1, 0, 'Look up word: ')
        curses.echo()
        userInput = bytes.decode(screen.getstr(), 'utf-8')
        curses.noecho()
        display(lookup(userInput))
        menu()
    elif chr(command) in 'qQ':
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()
        with open('historypickle', 'wb') as outfile:
            pickle.dump(history.history, outfile)
        quit()
    elif chr(command) in 'hH':
        history.viewHistory()
        menu()
    elif chr(command) in 'rR':
        display(lookup(random.choice(index)[1]))
    else:
        menu()

class Spellcheck:
    def __init__(self, word):
        global wordlist
        self.suggestions = wordlist.suggest(word)
        if len(self.suggestions) == 0:
            screen.clear()
            screen.addstr(word + " not found")
            screen.getch()
            menu()
        self.suggestions = [word + ' not found.  Did you mean:'] + self.suggestions

    def writeToScreen(self, offset):
        height = screen.getmaxyx()[0]
        self.positionList = []
        if offset < 0:
            begin = 0
        else:
            begin = offset
        if begin + height > len(self.suggestions):
            end = len(self.suggestions)
        else:
            end = begin + height
        screen.clear()
        for item in self.suggestions[begin:end]:
            screen.addstr(item)
            self.positionList.append((screen.getyx()[0], item))
            if screen.getyx()[0] != height -1:
                screen.addstr('\n')

    def view(self):
        offset = 0
        self.writeToScreen(offset)
        screen.move(0, 0)
        command = chr(screen.getch())
        position = 0
        while command not in 'qQ':
            if command in 'lL':
                for pair in self.positionList:
                    if position == pair[0]:
                        display(lookup(pair[1]))
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
        menu()

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
                        display(lookup(pair[1]))
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
