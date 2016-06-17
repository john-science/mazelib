
from __future__ import absolute_import
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo, i8
import cython
cimport numpy as cnp
import numpy as np
cnp.import_array()
from random import shuffle


cdef class Kruskal(MazeGenAlgo):

    def __cinit__(self, h, w):
        super(Kruskal, self).__init__(h, w)

    @cython.boundscheck(False)
    cpdef i8[:,:] generate(self):
        cdef int ce_row, ce_col, i, row, col, tree1, tree2
        cdef i8[:,:] grid

        # create empty grid
        a = np.empty((self.H, self.W), dtype=np.int8)
        a.fill(1)
        grid = a

        forest = []
        for row in range(1, self.H - 1, 2):
            for col in range(1, self.W -1, 2):
                forest.append([(row, col)])
                grid[row][col] = 0

        edges = []
        for row in range(2, self.H - 1, 2):
            for col in range(1, self.W - 1, 2):
                edges.append((row, col))
        for row in range(1, self.H - 1, 2):
            for col in range(2, self.W - 1, 2):
                edges.append((row, col))

        shuffle(edges)

        while len(forest) > 1:
            ce_row, ce_col = edges[0]
            edges = edges[1:]

            tree1 = -1
            tree2 = -1

            if ce_row % 2 == 0:  # even-numbered row: vertical wall
                #print(ce_row, ce_col)
                #print((ce_row - 1, ce_col))
                #print(999 if (ce_row - 1, ce_col) in forest[0] else 0)
                #print(forest)
                #print([(i,j) for i, j in enumerate(forest)])
                #print([i if (ce_row - 1, ce_col) in j else 0 for i, j in enumerate(forest)])
                tree1 = sum([i if (ce_row - 1, ce_col) in j else 0 for i, j in enumerate(forest)])
                tree2 = sum([i if (ce_row + 1, ce_col) in j else 0 for i, j in enumerate(forest)])
            else:  # odd-numbered row: horizontal wall
                #print(ce_row, ce_col)
                #print((ce_row, ce_col - 1))
                #print(777 if (ce_row, ce_col - 1) in forest[0] else 0)
                #print(forest)
                #print([(i,j) for i, j in enumerate(forest)])
                #print([i if (ce_row, ce_col - 1) in j else 0 for i, j in enumerate(forest)])
                tree1 = sum([i if (ce_row, ce_col - 1) in j else 0 for i, j in enumerate(forest)])
                tree2 = sum([i if (ce_row, ce_col + 1) in j else 0 for i, j in enumerate(forest)])

            if tree1 != tree2:
                new_tree = forest[tree1] + forest[tree2]
                temp1 = list(forest[tree1])
                temp2 = list(forest[tree2])
                forest = [x for x in forest if x != temp1]  # faster than forest.remove(temp1)
                forest = [x for x in forest if x != temp2]
                forest.append(new_tree)
                grid[ce_row][ce_col] = 0

        return grid
