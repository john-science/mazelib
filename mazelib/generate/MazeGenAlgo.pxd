cimport cython
from numpy cimport ndarray
cimport numpy as np


cdef class MazeGenAlgo:
    cpdef public int h
    cpdef public int w
    cpdef public int H
    cpdef public int W

    cpdef ndarray[cython.char, ndim=2] generate(self)  # TODO: Can we add type and dimensions to this?????

    @cython.locals(ns=list)
    cdef list _find_neighbors(self, int r, int c, ndarray[cython.char, ndim=2] grid, bint is_wall=*)
