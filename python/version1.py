"""
Version 1
"""

import curses
import time
import random

from environment import Environment
from fruit import Fruit
from agent import Agent

def main(stdscr):
    # Clear screen
    curses.curs_set(0) # invisible cursor
    curses.use_default_colors()
    stdscr.clear()

    # Define Colors
    curses.init_pair(0, 0, -1) # Base
    curses.init_pair(1, 1, -1) # A
    curses.init_pair(2, 2, -1) # B
    curses.init_pair(3, 3, -1) # Agent
    env = Environment(30, 30, stdscr)
    env.initialise_agents(40)
    env.initialise_fruits(200)
    env.update()
    env.display()

    ### Animation
    for i in range(int(2e4)):
        stdscr.addstr(0, 0, f'Iteration {i}\t')
        stdscr.refresh()
        random.shuffle(env.agents) # Shuffle to avoid bias
        for agent in env.agents:
            agent.act()
            env.update()
        env.display(2 * 30 + 8)

    stdscr.addstr(0, 0, 'Press any key to quit\t')
    stdscr.refresh()
    stdscr.getkey()


if __name__ == '__main__':
    curses.wrapper(main)
