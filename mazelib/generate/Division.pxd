cimport cython
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo
from numpy cimport ndarray
cimport numpy as np

# CONSTANTS
cdef cython.int VERTICAL = 0
cdef cython.int HORIZONTAL = 1



cdef class Division(MazeGenAlgo):

    @cython.locals(grid=ndarray, region_stack=list, current_region=tuple, region_stack=list, min_y=cython.int,
                   max_y=cython.int, min_x=cython.int, min_y=cython.int, height=cython.int, width=cython.int,
                   cut_direction=cython.int, cut_length=cython.int, cut_posi=cython.int, door_posi=cython.int,
                   row=cython.int, col=cython.int)
    cpdef ndarray[cython.char, ndim=2] generate(self)
