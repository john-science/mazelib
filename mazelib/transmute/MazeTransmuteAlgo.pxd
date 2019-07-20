cimport cython
from numpy cimport ndarray


cdef class MazeTransmuteAlgo:
    cdef public ndarray grid
    cdef public tuple start
    cdef public tuple end


    cpdef void transmute(self, ndarray[cython.char, ndim=2] grid, tuple start, tuple end)


    cpdef void _transmute(self)


    @cython.locals(r=cython.int, c=cython.int, ns=list)
    cpdef _find_unblocked_neighbors(self, tuple posi)


    @cython.locals(ns=list)
    cdef list _find_neighbors(self, int r, int c, bint is_wall=*)


    cpdef bint _within_one(self, tuple cell, tuple desire)


    cdef inline tuple _midpoint(self, tuple a, tuple b)
