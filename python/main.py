import curses
import time

class Environment:
    def __init__(self, n, m):
        self.grid = [[0 for j in range(m)] for i in range(n)]

    def display(self):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == 1:
                    stdscr.addstr(i, 2 * j, str(cell), curses.color_pair(1))
                else:
                    stdscr.addstr(i, 2 * j, str(cell))
                stdscr.refresh()


if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, 0)
    curses.noecho()
    curses.cbreak()

    env = Environment(5, 5)
    for i in range(5):
        env.grid[i][i] = 1
        env.display()
        time.sleep(0.5)


    curses.echo()
    curses.nocbreak()
    curses.endwin()
