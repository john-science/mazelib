import numpy as np
from random import randrange
# If the code is not Cython-compiled, we need to add some imports.
from cython import compiled
if not compiled:
    from mazelib.generate.MazeGenAlgo import MazeGenAlgo


class BacktrackingGenerator(MazeGenAlgo):
    """
    1. Randomly choose a starting cell.
    2. Randomly choose a wall at the current cell and open a passage through to any random adjacent
        cell, that has not been visited yet. This is now the current cell.
    3. If all adjacent cells have been visited, back up to the previous and repeat step 2.
    4. Stop when the algorithm has backed all the way up to the starting cell.
    """

    def __init__(self, w, h):
        super(BacktrackingGenerator, self).__init__(w, h)

    def generate(self):
        """ highest-level method that implements the maze-generating algorithm

        Returns:
            np.array: returned matrix
        """
        # create empty grid, with walls
        grid = np.empty((self.H, self.W), dtype=np.int8)
        grid.fill(1)

        crow = randrange(1, self.H, 2)
        ccol = randrange(1, self.W, 2)
        track = [(crow, ccol)]
        grid[crow][ccol] = 0

        while track:
            (crow, ccol) = track[-1]
            neighbors = self._find_neighbors(crow, ccol, grid, True)

            if len(neighbors) == 0:
                track = track[:-1]
            else:
                nrow, ncol = neighbors[0]
                grid[nrow][ncol] = 0
                grid[(nrow + crow) // 2][(ncol + ccol) // 2] = 0

                track += [(nrow, ncol)]

        return grid
