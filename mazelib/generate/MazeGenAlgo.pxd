cimport cython
#cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
from numpy cimport ndarray
cimport numpy as np


cdef class MazeGenAlgo:
    cpdef public int h
    cpdef public int w
    cpdef public int H
    cpdef public int W

    cpdef ndarray generate(self)

    @cython.locals(ns=list)
    cdef list _find_neighbors(self, int r, int c, ndarray[cython.short, ndim=2] grid, bint is_wall=*)
