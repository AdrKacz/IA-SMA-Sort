"""
Version 1
"""

import curses
import time
import random

from environment import Environment
from fruit import Fruit
from agent import Agent

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

    env = Environment(30, 30, stdscr)
    env.initialise_fruits(200)
    env.initialise_agents(40)
    env.update()
    env.display()

    ### Animation
    for i in range(int(2e4)):
        stdscr.addstr(0, 0, f'Iteration {i}\t')
        stdscr.refresh()
        random.shuffle(env.agents)
        for agent in env.agents:
            agent.act()
            env.update()
        env.display(2 * 30 + 8)
    time.sleep(100)

    curses.echo()
    curses.nocbreak()
    curses.endwin()
