cimport cython
from mazelib.transmute.MazeTransmuteAlgo cimport MazeTransmuteAlgo


cdef class DeadEndFiller(MazeTransmuteAlgo):
    cdef public cython.int iterations


    @cython.locals(r=cython.int, c=cython.int, found=cython.bint, i=cython.int,
                   start_save=cython.char, end_save=cython.char)
    cpdef void _transmute(self)


    @cython.locals(dead_end=tuple, ns=list, found=cython.int)
    cdef inline cython.int _fill_dead_ends(self)


    @cython.locals(r=cython.int, c=cython.int)
    cdef inline void _fill_dead_end(self, tuple dead_end)


    @cython.locals(r=cython.int, c=cython.int)
    cdef inline tuple _find_dead_end(self)


    @cython.locals(ns=list)
    cdef inline bint _is_dead_end(self, tuple cell)
