import curses

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

screen.getch()
curses.flash()
screen.getch()

curses.nocbreak()
screen.keypad(False)
curses.echo()
curses.endwin()
