import curses

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

longstring = """one
two
three
four
five
six
seven
eight
nine
ten
eleven
twelve
thirteen
fourteen
fifteen
sixteen
seventeen
eighteen
nineteen
twenty
twenty one
twenty two
twenty three
twenty four
twenty five
twenty six
twenty seven
twenty eight
twenty nine
thirty
"""
scrollythingy(longstring)
scrollythingy('blah')
scrollythingy('blah\nblah\nblah')

curses.nocbreak()
screen.keypad(False)
curses.echo()
curses.endwin()
