
from __future__ import absolute_import
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo, i8
import cython
cimport numpy as cnp
import numpy as np
cnp.import_array()
from random import choice, randrange


cdef class AldousBroder(MazeGenAlgo):
    """
    1. Choose a random cell.
    2. Choose a random neighbor of the current cell and visit it. If the neighbor has not
        yet been visited, add the traveled edge to the spanning tree.
    3. Repeat step 2 until all cells have been visited.
    """

    def __cinit__(self, h, w):
        super(AldousBroder, self).__init__(h, w)

    @cython.boundscheck(False)
    cpdef i8[:,:] generate(self):
        cdef int num_visited, current_row, current_col
        cdef i8[:,:] grid

        # create empty grid, with walls
        a = np.empty((self.H, self.W), dtype=np.int8)
        a.fill(1)
        grid = a

        current_row, current_col = randrange(1, self.H, 2), randrange(1, self.W, 2)
        grid[current_row][current_col] = 0
        num_visited = 1

        while num_visited < self.h * self.w:
            # find neighbors
            neighbors = self._find_neighbors((current_row, current_col), grid, True)

            # how many neighbors have already been visited?
            if len(neighbors) == 0:
                # mark random neighbor as current
                (current_row, current_col) = choice(self._find_neighbors((current_row, current_col), grid))
                continue

            # loop through neighbors
            for neighbor in neighbors:
                if grid[neighbor[0]][neighbor[1]] > 0:
                    # open up wall to new neighbor
                    grid[((neighbor[0]+current_row)//2, (neighbor[1]+current_col)//2)] = 0
                    # mark neighbor as visited
                    grid[neighbor[0]][neighbor[1]] = 0
                    # bump the number visited
                    num_visited += 1
                    # current becomes new neighbor
                    (current_row, current_col) = neighbor
                    # break loop
                    break

        return grid
