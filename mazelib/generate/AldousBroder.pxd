cimport cython
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo
from numpy cimport ndarray
cimport numpy as np


cdef class AldousBroder(MazeGenAlgo):

    @cython.locals(grid=ndarray, crow=cython.uint, ccol=cython.uint, nrow=cython.uint, ncol=cython.uint,
                   num_visited=cython.uint, neighbors=list)
    cpdef ndarray[cython.char, ndim=2] generate(self)
