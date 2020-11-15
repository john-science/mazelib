import numpy as np
from random import choice, randrange
# If the code is not Cython-compiled, we need to add some imports.
from cython import compiled
if not compiled:
    from mazelib.generate.MazeGenAlgo import MazeGenAlgo


class AldousBroder(MazeGenAlgo):
    """
    1. Choose a random cell.
    2. Choose a random neighbor of the current cell and visit it. If the neighbor has not
        yet been visited, add the traveled edge to the spanning tree.
    3. Repeat step 2 until all cells have been visited.
    """

    def __init__(self, h, w):
        super(AldousBroder, self).__init__(h, w)

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
        grid[crow][ccol] = 0
        num_visited = 1

        while num_visited < self.h * self.w:
            # find neighbors
            neighbors = self._find_neighbors(crow, ccol, grid, True)

            # how many neighbors have already been visited?
            if len(neighbors) == 0:
                # mark random neighbor as current
                (crow, ccol) = choice(self._find_neighbors(crow, ccol, grid))
                continue

            # loop through neighbors
            for nrow, ncol in neighbors:
                if grid[nrow][ncol] > 0:
                    # open up wall to new neighbor
                    grid[(nrow + crow) // 2][(ncol + ccol) // 2] = 0
                    # mark neighbor as visited
                    grid[nrow][ncol] = 0
                    # bump the number visited
                    num_visited += 1
                    # current becomes new neighbor
                    crow = nrow
                    ccol = ncol
                    # break loop
                    break

        return grid
