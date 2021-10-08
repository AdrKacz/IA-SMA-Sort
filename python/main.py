import curses
import time
import random

class Environment:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.grid = [[0 for j in range(m)] for i in range(n)]
        self.agents = list()
        self.fruits = list()

    def update(self):
        self.grid = [[0 for j in range(self.m)] for i in range(self.n)]
        for agent in self.agents:
            self.update_agent(agent)
        for fruit in self.fruits:
            self.update_fruit(*fruit)

    def update_agent(self, agent):
        assert not self.grid[agent.y][agent.x]
        self.grid[agent.y][agent.x] = 'X'

    def update_fruit(self, x, y, label):
        assert not self.grid[y][x]
        self.grid[y][x] = label

    def map_color(self, cell):
        if cell == 'A':
            return 1
        elif cell == 'B':
            return 2
        elif cell == 'X':
            return 3
        else:
            return 0

    def display(self):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell:
                    stdscr.addstr(i + 1, 2 * j, str(cell), curses.color_pair(self.map_color(cell)))
                else:
                    stdscr.addstr(i + 1, 2 * j, ' ')
                stdscr.refresh()
    def get_neighbors(self, x, y):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (dx or dy) and (0 <= x + dx < self.n and 0 <= y + dy < self.m) and not self.grid[y + dy][x + dx]:
                    yield x + dx, y + dy

class Agent:
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.memory = [0 for i in range(10)]
        self.parent = parent

    def act(self):
        neighbors = list(self.parent.get_neighbors(self.x, self.y))
        if len(neighbors) == 0:
            return
        self.x, self.y = random.choice(neighbors)



if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    curses.start_color()
    curses.use_default_colors()
    # Define Colors
    curses.init_pair(0, 0, -1) # Base
    curses.init_pair(1, 1, -1) # A
    curses.init_pair(2, 2, -1) # B
    curses.init_pair(3, 3, -1) # Agent

    env = Environment(10, 10)
    env.agents = [
    Agent(1, 0, env),
    Agent(4, 5, env),
    Agent(9, 8, env),
    ]
    env.fruits = [
    (0, 0, 'A'),
    (8, 7, 'A'),
    (4, 3, 'A'),
    (1, 6, 'B'),
    (3, 2, 'B'),
    (8, 1, 'B'),
    ]
    env.update()

    stdscr.addstr(0, 0, f'Initial State')
    stdscr.refresh()
    env.display()
    time.sleep(1)
    for i in range(30):
        stdscr.addstr(0, 0, f'Iteration {i}\t')
        stdscr.refresh()
        random.shuffle(env.agents)
        for agent in env.agents:
            agent.act()
            env.update()
        env.display()
        time.sleep(0.5)

    curses.echo()
    curses.nocbreak()
    curses.endwin()
