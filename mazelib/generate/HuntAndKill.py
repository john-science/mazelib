
from random import choice, randrange, shuffle
import numpy as np
# If the code is not Cython-compiled, we need to add some imports.
try:
    from cython import compiled
except ModuleNotFoundError:
    compiled = False
if not compiled:
    from mazelib.generate.MazeGenAlgo import MazeGenAlgo

RANDOM = 1
SERPENTINE = 2


class HuntAndKill(MazeGenAlgo):
    """
    1. Randomly choose a starting cell.
    2. Perform a random walk from the current cel, carving passages to unvisited neighbors,
        until the current cell has no unvisited neighbors.
    3. Select a new grid cell; if it has been visited, walk from it.
    4. Repeat steps 2 and 3 a sufficient number of times that there the probability of a cell
        not being visited is extremely small.

    In this implementation of Hunt-and-kill there are two different ways to select a new grid
        cell in step 2.  The first is serpentine through the grid (the classic solution), the
        second is to randomly select a new cell enough times that the probability of an
        unexplored cell is very, very low. The second option includes a small amount of risk,
        but it creates a more interesting, harder maze.
    """

    def __init__(self, w, h, hunt_order='random'):
        super(HuntAndKill, self).__init__(w, h)

        # the user can define what order to hunt for the next cell in
        if hunt_order.lower().strip() == 'serpentine':
            self.ho = SERPENTINE
        else:
            self.ho = RANDOM

    def generate(self):
        # create empty grid
        grid = np.empty((self.H, self.W), dtype=np.int8)
        grid.fill(1)

        # find an arbitrary starting position
        current_row, current_col = (randrange(1, self.H, 2), randrange(1, self.W, 2))
        grid[current_row][current_col] = 0

        # perform many random walks, to fill the maze
        num_trials = 0
        while (current_row, current_col) != (-1, -1):
            self._walk(grid, current_row, current_col)
            current_row, current_col = self._hunt(grid, num_trials)
            num_trials += 1

        return grid

    def _walk(self, grid, row, col):
        """
        This is a standard random walk. It must start from a visited cell.
        And it completes when the current cell has no unvisited neighbors.
        """
        if grid[row][col] == 0:
            this_row = row
            this_col = col
            unvisited_neighbors = self._find_neighbors(this_row, this_col, grid, True)

            while len(unvisited_neighbors) >  0:
                neighbor = choice(unvisited_neighbors)
                grid[neighbor[0]][neighbor[1]] = 0
                grid[(neighbor[0] + this_row) // 2][(neighbor[1] + this_col) // 2] = 0
                this_row, this_col = neighbor
                unvisited_neighbors = self._find_neighbors(this_row, this_col, grid, True)

    def _hunt(self, grid, count):
        """ Based on how this algorithm was configured, choose hunt for the next starting point. """
        if self.ho == SERPENTINE:
            return self._hunt_serpentine(grid, count)
        else:
            return self._hunt_random(grid, count)

    def _hunt_random(self, grid, count):
        """ Select the next cell to walk from, randomly. """
        if count >= (self.H * self.W):
            return (-1, -1)

        return (randrange(1, self.H, 2), randrange(1, self.W, 2))

    def _hunt_serpentine(self, grid, count):
        """ Select the next cell to walk from by cycling through every grid cell in order. """
        row, col = (1, 1)
        found = False

        while not found:
            col = col + 2
            if col > (self.W - 2):
                row += 2
                col = 1
                if row > (self.H - 2):
                    return (-1, -1)

            if grid[row][col] == 0 and len(self._find_neighbors(row, col, grid, True)) > 0:
                found = True

        return (row, col)
