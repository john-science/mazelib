cimport cython
from numpy cimport ndarray


cdef class MazeSimplifyAlgo:
    cdef public ndarray grid
    cdef public tuple start
    cdef public tuple end


    cpdef void simplify(self, ndarray[cython.char, ndim=2] grid, tuple start, tuple end)


    cpdef void _simplify(self)


    @cython.locals(r=cython.int, c=cython.int, ns=list)
    cpdef _find_unblocked_neighbors(self, tuple posi)


    cpdef bint _within_one(self, tuple cell, tuple desire)
