cimport cython
from mazelib.solve.MazeSolveAlgo cimport MazeSolveAlgo
from mazelib.solve.ShortestPaths cimport ShortestPaths


cdef class DeadEndFiller(MazeSolveAlgo):
    cdef readonly MazeSolveAlgo solver


    @cython.locals(r=cython.int, c=cython.int)
    cpdef list _solve(self)


    cdef inline list _build_solutions(self)


    @cython.locals(dead_end=tuple, ns=list)
    cdef inline void _fill_dead_ends(self)


    @cython.locals(r=cython.int, c=cython.int)
    cdef inline void _fill_dead_end(self, tuple dead_end)


    @cython.locals(r=cython.int, c=cython.int)
    cdef inline tuple _find_dead_end(self)


    @cython.locals(ns=list)
    cdef inline bint _is_dead_end(self, tuple cell)
