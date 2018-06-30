cimport cython
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo
from numpy cimport ndarray
cimport numpy as np


cdef class BinaryTree(MazeGenAlgo):
    cdef readonly list skew

    @cython.locals(grid=ndarray, row=cython.uint, col=cython.uint, neighbor_row=cython.uint, neighbor_col=cython.uint)
    cpdef ndarray[cython.char, ndim=2] generate(self)

    @cython.locals(neighbors=list, neighbor_row=cython.uint, neighbor_col=cython.uint, b_row=cython.int,
                   b_col=cython.int, current_row=cython.uint, current_col=cython.uint)
    cdef inline tuple _find_neighbor(self, cython.uint current_row, cython.uint current_col)
