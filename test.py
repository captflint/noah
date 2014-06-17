import curses

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
screen.refresh()

height = screen.getmaxyx()[0] - 1
width = screen.getmaxyx()[1] - 1
position = [0, 0]
command = 0
while chr(command) not in 'qQ':
    command = screen.getch()
    if chr(command) in 'wW':
        if position[0] == 0:
            curses.flash()
        else:
            position[0] -= 1
    elif chr(command) in 'aA':
        if position[1] == 0:
            curses.flash()
        else:
            position[1] -= 1
    elif chr(command) in 'sS':
        if position[0] == height:
            curses.flash()
        else:
            position[0] += 1
    elif chr(command) in 'dD':
        if position[1] == width:
            curses.flash()
        else:
            position[1] += 1
    screen.move(position[0], position[1])

curses.nocbreak()
screen.keypad(False)
curses.echo()
curses.endwin()
