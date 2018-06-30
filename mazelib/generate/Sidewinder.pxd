cimport cython
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo
from numpy cimport ndarray
cimport numpy as np


cdef class Sidewinder(MazeGenAlgo):
    cdef readonly double skew

    @cython.locals(grid=ndarray, col=cython.int, row=cython.int, run=list, carve_east=bint,
                   north=tuple)
    cpdef ndarray[cython.char, ndim=2] generate(self)
