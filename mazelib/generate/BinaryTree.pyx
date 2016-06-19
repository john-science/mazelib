
from __future__ import absolute_import
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo, i8
import cython
cimport numpy as cnp
import numpy as np
cnp.import_array()
from random import choice


cdef class BinaryTree(MazeGenAlgo):

    def __cinit__(self, w, h, bias=None):
        super(BinaryTree, self).__init__(w, h)
        biases = {'NW': [(1, 0), (0, -1)],
                  'NE': [(1, 0), (0, 1)],
                  'SW': [(-1, 0), (0, -1)],
                  'SE': [(-1, 0), (0, 1)]}
        if bias in biases.keys():
            self.bias = biases[bias]
        else:
            key = choice(list(biases.keys()))
            self.bias = biases[key]

    @cython.boundscheck(False)
    cpdef i8[:,:] generate(self):
        cdef int row, col, neighbor_row, neighbor_col
        cdef i8[:,:] grid

        # create empty grid, with walls
        a = np.empty((self.H, self.W), dtype=np.int8)
        a.fill(1)
        grid = a

        for row in range(1, self.H, 2):
            for col in range(1, self.W, 2):
                grid[row][col] = 0
                neighbor_row, neighbor_col = self._find_neighbor(row, col)
                grid[neighbor_row][neighbor_col] = 0

        return grid

    cdef tuple _find_neighbor(self, int current_row, int current_col):
        """ Find a neighbor in the biased direction.
        """
        cdef b_row, b_col, neighbor_row, neighbor_col
        neighbors = []
        for b_row, b_col in self.bias:
            neighbor_row = current_row + b_row
            neighbor_col = current_col + b_col
            if neighbor_row > 0 and neighbor_row < (self.H - 1):
                if neighbor_col > 0 and neighbor_col < (self.W - 1):
                    neighbors.append((neighbor_row, neighbor_col))

        if len(neighbors) == 0:
            return (current_row, current_col)
        else:
            return choice(neighbors)
