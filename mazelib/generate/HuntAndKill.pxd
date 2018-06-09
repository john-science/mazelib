cimport cython
#cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo
from numpy cimport ndarray
cimport numpy as np


cdef class HuntAndKill(MazeGenAlgo):
    cdef readonly cython.int ho

    @cython.locals(grid=ndarray, num_trails=cython.int, current_row=cython.int, current_col=cython.int)
    cpdef ndarray[cython.char, ndim=2] generate(self)

    @cython.locals(this_row=cython.int, this_col=cython.int, unvisited_neighbors=list, neighbor=tuple)
    cdef inline void _walk(self, ndarray[cython.char, ndim=2] grid, cython.int row, cython.int col)

    cdef inline tuple _hunt(self, ndarray[cython.char, ndim=2] grid, cython.int count)

    cdef inline tuple _hunt_random(self, ndarray[cython.char, ndim=2] grid, cython.int count)

    @cython.locals(row=cython.int, col=cython.int, found=bint)
    cdef inline tuple _hunt_serpentine(self, ndarray[cython.char, ndim=2] grid, cython.int count)
