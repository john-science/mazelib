
from random import randrange
import numpy as np
# If the code is not Cython-compiled, we need to add some imports.
try:
    from cython import compiled
except ModuleNotFoundError:
    compiled = False
if not compiled:
    from mazelib.generate.MazeGenAlgo import MazeGenAlgo


class Prims(MazeGenAlgo):
    """
    The Algorithm

    1. Choose an arbitrary cell from the grid, and add it to some
        (initially empty) set visited nodes (V).
    2. Randomly select a wall from the grid that connects a cell in
        V with another cell not in V.
    3. Add that wall to the Minimal Spanning Tree (MST), and the edge's other cell to V.
    4. Repeat steps 2 and 3 until V includes every cell in G.
    """

    def __init__(self, h, w):
        super(Prims, self).__init__(h, w)

    def generate(self):
        # create empty grid
        grid = np.empty((self.H, self.W), dtype=np.int8)
        grid.fill(1)

        # choose a random starting position
        current_row = randrange(1, self.H, 2)
        current_col = randrange(1, self.W, 2)
        grid[current_row][current_col] = 0

        # created a weighted list of all vertices connected in the graph
        neighbors = self._find_neighbors(current_row, current_col, grid, True)

        # loop over all current neighbors, until empty
        visited = 1

        while visited < self.h * self.w:
            # find neighbor with lowest weight, make it current
            nn = randrange(len(neighbors))
            current_row, current_col = neighbors[nn]
            visited += 1
            grid[current_row][current_col] = 0
            neighbors = neighbors[:nn] + neighbors[nn + 1:]
            # connect that neighbor to a random neighbor with grid[posi] == 0
            nearest_n0, nearest_n1 = self._find_neighbors(current_row, current_col, grid)[0]
            grid[(current_row + nearest_n0) // 2][(current_col + nearest_n1) // 2] = 0

            # find all unvisited neighbors of current, add them to neighbors
            unvisited = self._find_neighbors(current_row, current_col, grid, True)
            neighbors = list(set(neighbors + unvisited))

        return grid
