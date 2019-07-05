
from random import choice, randrange
from numpy.random import shuffle
import numpy as np
# If the code is not Cython-compiled, we need to add some imports.
try:
    from cython import compiled
except ModuleNotFoundError:
    compiled = False
if not compiled:
    from mazelib.generate.MazeGenAlgo import MazeGenAlgo


class CellularAutomaton(MazeGenAlgo):
    """ Cells survive if they have one to four neighbours.
    If a cell has exactly three neighbours, it is born.

    It is similar to Conway's Game of Life in that patterns
    that do not have a living cell adjacent to 1, 4, or 5 other
    living cells in any generation will behave identically to it.
    """

    def __init__(self, w, h, complexity=1.0, density=1.0):
        super(CellularAutomaton, self).__init__(w, h)
        self.complexity = complexity
        self.density = density

    def generate(self):
        # create empty grid
        grid = np.empty((self.H, self.W), dtype=np.int8)
        grid.fill(0)
        # fill borders
        grid[0, :] = grid[-1, :] = 1
        grid[:, 0] = grid[:, -1] = 1

        # adjust complexity and density relative to maze size
        if self.complexity <= 1.0:
            self.complexity = self.complexity * 10 * (self.H + self.W)
        if self.density <= 1.0:
            self.density = self.density * (self.h * self.w)

        # create walls
        for i in range(int(self.density)):
            y, x = randrange(0, self.H, 2), randrange(0, self.W, 2)
            grid[y, x] = 1
            for j in range(int(self.complexity)):
                neighbors = self._find_neighbors(y, x, grid, True)  # is wall
                if len(neighbors) > 0 and len(neighbors) < 5:
                    neighbors = self._find_neighbors(y, x, grid)       # is open
                    if not len(neighbors):
                        continue
                    r,c = choice(neighbors)
                    if grid[r, c] == 0:
                        grid[r, c] = 1
                        grid[r + (y - r) // 2, c + (x - c) // 2] = 1
                        x, y = c, r

        return grid
