cimport cython
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo
from numpy cimport ndarray
cimport numpy as np


cdef class CellularAutomaton(MazeGenAlgo):
    cdef readonly cython.double complexity
    cdef readonly cython.double density

    @cython.locals(grid=ndarray, i=cython.int, j=cython.int, x=cython.int, y=cython.int,
                   neighbors=list, r=cython.int, c=cython.int)
    cpdef ndarray[cython.char, ndim=2] generate(self)
