cimport cython
from mazelib.solve.MazeSolveAlgo cimport MazeSolveAlgo
from mazelib.solve.DeadEndFiller cimport DeadEndFiller
from mazelib.solve.ShortestPaths cimport ShortestPaths


cdef class CuldeSacFiller(MazeSolveAlgo):
    cdef readonly MazeSolveAlgo solver


    @cython.locals(r=cython.int, c=cython.int, ns=list, end1=tuple, end2=tuple)
    cpdef list _solve(self)


    @cython.locals(first=tuple, previous=tuple, current=tuple, ns=list)
    cdef inline tuple _find_next_intersection(self, list path_start)
