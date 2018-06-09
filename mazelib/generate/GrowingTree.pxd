cimport cython
#cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo
from numpy cimport ndarray
cimport numpy as np


cdef class GrowingTree(MazeGenAlgo):
    cdef readonly double backtrack_chance

    @cython.locals(grid=ndarray, current_row=cython.int, current_col=cython.int, nn_row=cython.int, nn_col=cython.int,
                   active=list, next_neighbors=list)
    cpdef ndarray[cython.char, ndim=2] generate(self)
