# Sorting with Multi-Agents System

## How to execute the code

The project doesn't need any external dependencies.
Be sure to have your terminal **full screen** and **color enabled** (use *PowerShell* on Windows)
```
git clone <link of the git repo>
cd python
python3 version1.py
python3 version2.py
```

You can stop the execution with `Ctrl-C` while it is running or press any key if it is done.

The initial 2D-grid is on the left side and the current 2D-grid is on the right side.

The code is pretty much self explanatory, don't hesitate to go through it to grasp what's under the hood.

*You can change the `width` and the `height` of the 2D-grid in either `version1.py` or `version2.py`. Try to keep the width small enough so that two grids can fit on your screens side-to-side (if not, that won't change the anything but it will be harder to see the animation).*

## From random grid to sorted grid

We have a 2D-grid filled randomly fruits of different types.
We want a group of agent to sort these fruits by type. Each agent is not aware of the global state of the 2D-grid.

### How to define the problem

We define three `class` for this problem.

- `Environment` that keeps the global state of display it on the terminal with the `curses` library.
- `Agent` that acts based on its neighbourhood.
- `Fruit` that can be carried by `Agent` and have a type that define their colour on the screen.

To correctly display and refresh the information in the terminal, we use `curses.wrapper` to call our main loop. It returns a `stdscr` used by `Environment` to print at any position and to refresh the screen.

### The main loop

At first, we initialise some values to hide the cursor and define the colours.

Then, we define the **environment** with its size and filled it with **agents** and **fruits**.

To fill the **environment**, we provide the desire number of element. If there is no more space left, some element won't be created.

The number of iteration is fixed. There is no way for the agents to determine if the 2D-grid is sorted or not, and we decided to avoid to add logic to evaluate how well fruits are gather in cluster in the grid.

On each iteration, each agent act based on its surrounding environment. To avoid any bias, the order in which the agents act is changed for each iteration.

After each action, we update the state of the environment to keep its information up to date for the following agents.

### Let's look them sort

## Some heavy fruits

Some fruits are heavy and need two agents to move them. Each agent can diffuse around its position signal to call for help, but can't call specifically any other agent. Each agent can detect signals but cannot dissociate any signals from any agents (not even from their signals).

### Let's look them sort
