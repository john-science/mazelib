cimport cython
from numpy cimport ndarray
cimport numpy as np


cdef class MazeGenAlgo:
    cdef public int h
    cdef public int w
    cdef public int H
    cdef public int W

    cpdef ndarray[cython.char, ndim=2] generate(self)

    @cython.locals(ns=list)
    cdef list _find_neighbors(self, int r, int c, ndarray[cython.char, ndim=2] grid, bint is_wall=*)
