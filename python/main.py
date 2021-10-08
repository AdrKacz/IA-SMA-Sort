import curses
import time

class Environment:
    def __init__(self, n, m):
        self.grid = [[None for j in range(m)] for i in range(n)]

    def map_color(self, cell):
        if cell == 'A':
            return 1
        elif cell == 'B':
            return 2
        elif cell == 'O':
            return 3
        else:
            return 0

    def display(self):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell:
                    stdscr.addstr(i, 2 * j, str(cell), curses.color_pair(self.map_color(cell)))
                    stdscr.refresh()

class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.memory = [0 for i in range(10)]

    def act(self):
        pass


if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    curses.start_color()
    curses.use_default_colors()
    # Define Colors
    curses.init_pair(0, 0, -1) # Base
    curses.init_pair(1, 1, -1) # A
    curses.init_pair(1, 2, -1) # B
    curses.init_pair(1, 3, -1) # Agent

    env = Environment(5, 5)
    agents = list()

    grid.display()
    time.sleep(1)
    for i in range(100):
        agents.shuffle()
        for agent in agents:
            agent.act()
        grid.display()
        time.sleep(0.5)

    curses.echo()
    curses.nocbreak()
    curses.endwin()
