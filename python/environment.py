import random

from curses import color_pair

from fruit import Fruit
from agent import Agent

stdscr = None

class Environment:
    def __init__(self, n, m, s):
        global stdscr
        stdscr = s
        self.n = n
        self.m = m
        self.grid = [[0 for j in range(m)] for i in range(n)]
        self.agents = list()
        self.fruits = list()

    def generate_item(self, desired_number, assign_function, R=10):
        for n in range(desired_number):
            x, y = random.randint(0, self.m - 1), random.randint(0, self.n - 1)
            r = 0
            while r < R and self.grid[y][x]:
                # Try at most R times
                x, y = random.randint(0, self.m - 1), random.randint(0, self.n - 1)
                r += 1
            if not self.grid[y][x]:
                assign_function(x, y)

    def initialise_agents(self, number_of_agent, R=10):
        def assign(x, y):
            assert not self.grid[y][x]
            self.agents.append(Agent(x, y, self))
            self.grid[y][x] = 'X'
        self.generate_item(number_of_agent, assign, R)

    def initialise_fruits(self, number_of_fruit, p_A=0.5, R=10):
        def assign(x, y):
            assert not self.grid[y][x]
            key_fruit = 'A' if random.random() < p_A else 'B'
            self.fruits.append(Fruit(x, y, key_fruit))
            self.grid[y][x] = key_fruit
        self.generate_item(number_of_fruit, assign, R)

    def update(self):
        self.grid = [[0 for j in range(self.m)] for i in range(self.n)]
        for agent in self.agents:
            self.update_agent(agent)
        for fruit in self.fruits:
            self.update_fruit(fruit)

    def update_agent(self, agent):
        assert not self.grid[agent.y][agent.x]
        self.grid[agent.y][agent.x] = agent

    def update_fruit(self, fruit):
        if not fruit.is_carried:
            assert not self.grid[fruit.y][fruit.x]
            self.grid[fruit.y][fruit.x] = fruit.key

    def display(self, x_shift=0):
        for i in range(self.n):
            for j in range(self.m):
                stdscr.addstr(i + 1, 2 * j + x_shift, ' ')

        for agent in self.agents:
            stdscr.addstr(agent.y + 1, 2 * agent.x + x_shift, 'X', color_pair(agent.color))

        for fruit in self.fruits:
            if not fruit.is_carried:
                stdscr.addstr(fruit.y + 1, 2 * fruit.x + x_shift, fruit.key, color_pair(fruit.color))

        stdscr.refresh()

    def get_neighbors(self, x, y, r=1):
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                if (dx or dy) and (0 <= x + dx < self.n and 0 <= y + dy < self.m):
                    yield x + dx, y + dy

    def get_empty_neighbors(self, x, y):
        for new_x, new_y in self.get_neighbors(x, y):
            if not self.grid[new_y][new_x]:
                    yield new_x, new_y

    def get_fruit_neighbors(self, x, y):
        for fruit in self.fruits:
            if not fruit.is_carried and abs(fruit.x - x) <= 1 and abs(fruit.y - y) <= 1:
                yield fruit
