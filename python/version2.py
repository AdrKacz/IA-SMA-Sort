"""
Version 1
"""

import curses
import time
import random

from environment import Environment
from fruit import Fruit
from agent import Agent

from curses import color_pair
stdscr = None

class HelperAgent(Agent):
    heavy_fruit_key = 'C'
    skip_heavy_fruit_rate = .1
    diffusion_distance = 3

    def __init__(self, x, y, parent):
        Agent.__init__(self, x, y, parent)
        Agent.is_helping = False

    def will_carry(self, key):
        frequency = self.get_frequency(key)
        rate = (Agent.k_plus / (Agent.k_plus + frequency)) ** 2
        if key == HelperAgent.heavy_fruit_key:
            return random.random() < rate * (1. - HelperAgent.skip_heavy_fruit_rate)
        else:
            return random.random() < rate

    def release_signals(self):
        for x, y in self.parent.get_neighbors(self.x, self.y, HelperAgent.diffusion_distance):
            distance = max(abs(x - self.x), abs(y - self.y)) - 1
            self.parent.add_signal(x, y, 1 - distance / HelperAgent.diffusion_distance)

    def act(self):
        # TODO: Switch main agent when blocked
        if self.is_helping: # Controlled by its main agent
            return
        empty_neighbors = list(self.parent.get_empty_neighbors(self.x, self.y))
        fruit_neighbors = list(self.parent.get_fruit_neighbors(self.x, self.y))
        key_fruit = 0
        if len(fruit_neighbors) > 0:
            key_fruit = random.choice(fruit_neighbors).key

        # Update memory
        while len(self.memory) >= Agent.memory_length:
            self.memory.pop(0)
        self.memory.append(key_fruit)

        if len(empty_neighbors) == 0:
            fruit = None
            for f in fruit_neighbors:
                if f.key == HelperAgent.heavy_fruit_key and self.will_carry(f.key):
                    fruit = f
                    break
            if fruit: # Heavy fruit
                # Stay in place and release signals
                self.release_signals()
            return

        # Move
        old_x, old_y = self.x, self.y
        self.x, self.y = random.choice(empty_neighbors)
        # If carry heavy fruit, release, else look around
        if self.fruit:
            # If heavy fruit, release, else move helper
            if self.fruit.key == HelperAgent.heavy_fruit_key:
                if self.will_release():
                    # Release fruit
                    self.fruit.x, self.fruit.y = old_x, old_y
                    self.color = Agent.color
                    self.fruit.is_carried = False
                    self.fruit = None
                    # Release helper
                    self.helper.is_helping = False
                    self.helper.color = Agent.color
                else:
                    # If fruit is heavy, helper must be defined
                    assert type(self.helper) == HelperAgent
                    self.helper.x, self.helper.y = old_x, old_y
            else:
                if self.will_release(): # Release fruit
                    self.fruit.x, self.fruit.y = old_x, old_y
                    self.color = Agent.color # Release
                    self.fruit.is_carried = False
                    self.fruit = None
        else:
            # Choose a fruit
            fruit = None
            for f in fruit_neighbors:
                if self.will_carry(f.key):
                    fruit = f
                    break

            if fruit:
                if fruit.key == HelperAgent.heavy_fruit_key: # If is heavy
                    # Look if there is someone around the fruit
                    for x, y in self.parent.get_neighbors(fruit.x, fruit.y):
                        if type(self.parent.grid[y][x]) == HelperAgent and not self.parent.grid[y][x] is self:
                            # Found someone to help
                            self.helper = self.parent.grid[y][x]
                            self.parent.grid[y][x].is_helping = True

                            self.x, self.y = fruit.x, fruit.y # Move on fruit
                            self.color = fruit.color
                            self.helper.color = fruit.color
                            fruit.is_carried = True
                            self.fruit = fruit

                            return

                    # Else stay in place and release signals
                    self.x, self.y = old_x, old_y
                    self.release_signals()

                else:  # Carry this fruit (new_key)
                    self.x, self.y = fruit.x, fruit.y # Move on fruit
                    self.color = fruit.color
                    fruit.is_carried = True
                    self.fruit = fruit
            else: # Look for signals
                signal_neighbors = [(x, y, self.parent.signal_grid[y][x]) for x, y in list(self.parent.get_neighbors(old_x, old_y))]
                assert 1 <= len(signal_neighbors) <= 8
                random.shuffle(signal_neighbors)
                signal_neighbors.sort(key=lambda signal: signal[2])
                i = 1
                signal = None
                while i < len(signal_neighbors) + 1 and signal_neighbors[-i][2] > 0:
                    # There is a signal to follow
                    if not self.parent.grid[signal_neighbors[-i][1]][signal_neighbors[-i][0]]:
                        signal = signal_neighbors[-i]
                        break
                    i += 1
                if signal:
                    self.x, self.y = signal[0], signal[1]





class ComplexEnvironment(Environment):
    decay_rate = 0.1

    def __init__(self, n, m, s):
        global stdscr
        stdscr = s
        Environment.__init__(self, n, m, s)
        self.signal_grid = [[0 for j in range(m)] for i in range(n)]

    def decay_signals(self):
        for i in range(self.n):
            for j in range(self.m):
                self.signal_grid[i][j] = max(0, self.signal_grid[i][j] - ComplexEnvironment.decay_rate)

    def display(self, x_shift=0):
        # TODO: Color in function of intensity
        for i in range(self.n):
            for j in range(self.m):
                if self.signal_grid[i][j] > 0:
                    stdscr.addstr(i + 1, 2 * j + x_shift, ' ', color_pair(5))
                else:
                    stdscr.addstr(i + 1, 2 * j + x_shift, ' ')

        for agent in self.agents:
            stdscr.addstr(agent.y + 1, 2 * agent.x + x_shift, 'X', color_pair(agent.color))

        for fruit in self.fruits:
            if not fruit.is_carried:
                stdscr.addstr(fruit.y + 1, 2 * fruit.x + x_shift, fruit.key, color_pair(fruit.color))

        stdscr.refresh()

    def initialise_agents(self, number_of_agent, R=10):
        def assign(x, y):
            assert not self.grid[y][x]
            self.agents.append(HelperAgent(x, y, self))
            self.grid[y][x] = 'X'
        self.generate_item(number_of_agent, assign, R)

    def initialise_fruits(self, number_of_fruit, R=10):
        def assign(x, y):
            assert not self.grid[y][x]
            key_fruit = random.choice(['A', 'B', 'C'])
            self.fruits.append(Fruit(x, y, key_fruit))
            self.grid[y][x] = key_fruit
        self.generate_item(number_of_fruit, assign, R)

    def add_signal(self, x, y, intensity):
        self.signal_grid[y][x] = min(1, self.signal_grid[y][x] + intensity)

def main(stdscr):
    # Clear screen
    curses.curs_set(0) # invisible cursor
    curses.use_default_colors()
    stdscr.clear()

    # Define Colors
    curses.init_pair(0, 0, -1) # Base
    curses.init_pair(1, 1, -1) # Agent
    curses.init_pair(2, 2, -1) # A
    curses.init_pair(3, 3, -1) # B
    curses.init_pair(4, 4, -1) # C

    curses.init_pair(5, -1, 5) # Signal
    # Define size
    width, height = 30, 30
    env = ComplexEnvironment(height, width, stdscr)
    env.initialise_agents(40)
    env.initialise_fruits(200)
    env.update()
    env.display() # display initial on the left

    ### Animation
    for i in range(int(2e4)):
        stdscr.addstr(0, 0, f'Iteration {i}\t')
        stdscr.refresh()
        env.decay_signals()
        random.shuffle(env.agents)
        for agent in env.agents:
            agent.act()
            env.update()
        env.display(2 * width + 8) # display on the right

    stdscr.addstr(0, 0, 'Press any key to quit\t')
    stdscr.refresh()
    stdscr.getkey()


if __name__ == '__main__':
    curses.wrapper(main)
