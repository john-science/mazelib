
from random import choice, random
import numpy as np
# If the code is not Cython-compiled, we need to add some imports.
try:
    from cython import compiled
except ModuleNotFoundError:
    compiled = False
if not compiled:
    from mazelib.generate.MazeGenAlgo import MazeGenAlgo


class Sidewinder(MazeGenAlgo):
    """
    The Algorithm

    1. Work through the grid row-wise, starting with the cell at 0,0.
    2. Add the current cell to a "run" set.
    3. For the current cell, randomly decide whether to carve East.
    4. If a passage East was carved, make the new cell the current cell and repeat steps 2-4.
    5. If a passage East was not carved, choose any one of the cells in the run set and carve
        a passage North. Then empty the run set. Repeat steps 2-5.
    6. Continue until all rows have been processed.

    Optional Parameters

    skew: Float [0.0, 1.0]
        If the skew is set less than 0.5 the maze will be skewed East-West, if it set greater
        than 0.5 it will be skewed North-South. (default 0.5)
    """

    def __init__(self, h, w, skew=0.5):
        super(Sidewinder, self).__init__(h, w)
        self.skew = skew

    def generate(self):
        # create empty grid
        grid = np.empty((self.H, self.W), dtype=np.int8)
        grid.fill(1)

        # The first row is always empty, because you can't carve North
        for col in range(1, self.W - 1):
            grid[1][col] = 0

        # loop through the remaining rows and columns
        for row in range(3, self.H, 2):
            # create a run of cells
            run = []

            for col in range(1, self.W, 2):
                # remove the wall to the current cell
                grid[row][col] = 0
                # add the current cell to the run
                run.append((row, col))

                carve_east = random() > self.skew
                # carve East or North (can't carve East into the East wall
                if carve_east and col < (self.W - 2):
                    grid[row][col + 1] = 0
                else:
                    north = choice(run)
                    grid[north[0] - 1][north[1]] = 0
                    run = []

        return grid
