from random import choice, randrange
import numpy as np
# If the code is not Cython-compiled, we need to add some imports.
from cython import compiled
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
        """ highest-level method that implements the maze-generating algorithm

        Returns:
            np.array: returned matrix
        """
        # create empty grid
        grid = np.empty((self.H, self.W), dtype=np.int8)
        grid.fill(0)
        # fill borders
        grid[0, :] = grid[-1, :] = 1
        grid[:, 0] = grid[:, -1] = 1

        # adjust complexity and density relative to maze size
        if self.complexity <= 1.0:
            self.complexity = self.complexity * (self.h + self.w)
        if self.density <= 1.0:
            self.density = self.density * (self.h * self.w)

        # create walls
        for i in range(int(2 * self.density)):
            # choose a starting location
            if i < (self.density):
                # we want to make sure we have a lot of walls that touch the outsie of the maze
                if choice([0, 1]):
                    y = choice([0, self.H - 1])
                    x = randrange(0, self.W, 2)
                else:
                    x = choice([0, self.W - 1])
                    y = randrange(0, self.H, 2)
            else:
                # let's try to fill in any voids we left in the maze
                y, x = randrange(0, self.H, 2), randrange(0, self.W, 2)

            # build a wall through the maze
            grid[y, x] = 1
            for j in range(int(self.complexity)):
                neighbors = self._find_neighbors(y, x, grid, True)  # is wall
                if len(neighbors) > 0 and len(neighbors) < 4:
                    neighbors = self._find_neighbors(y, x, grid, False)  # is open
                    if not len(neighbors):
                        continue
                    r, c = choice(neighbors)
                    if grid[r, c] == 0:
                        grid[r, c] = 1
                        grid[r + (y - r) // 2, c + (x - c) // 2] = 1
                        x, y = c, r

        return grid