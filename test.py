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
    while chr(command) not in 'Qq':
        screen.addstr(str(command))
        command = screen.getch()
        screen.clear()

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
scrollythingy('blahblahblah')

curses.nocbreak()
screen.keypad(False)
curses.echo()
curses.endwin()
