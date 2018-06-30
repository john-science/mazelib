cimport cython
from mazelib.solve.MazeSolveAlgo cimport MazeSolveAlgo


cdef class BacktrackingSolver(MazeSolveAlgo):
    cdef readonly bint prune

    @cython.locals(solution=list, current=tuple, ns=list, nxt=tuple)
    cpdef list _solve(self)


    @cython.locals(i=cython.int)
    cdef inline list _fix_entrances(self, list solution)
