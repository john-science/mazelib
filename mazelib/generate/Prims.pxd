cimport cython
#cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo
from numpy cimport ndarray


cdef class Prims(MazeGenAlgo):

    @cython.locals(grid=ndarray, current_row=cython.int, current_col=cython.int, visited=cython.int,
                   nearest_n0=cython.int, nearest_n1=cython.int, unvisited=list, neighbors=list, nn=cython.int)
    cpdef ndarray generate(self)
