import curses

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

screen.getch()
screen.scrollok(True)
screen.addstr("""one
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
""")
screen.getch()

curses.nocbreak()
screen.keypad(False)
curses.echo()
curses.endwin()
