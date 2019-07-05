from random import choice, shuffle
cimport cython
from mazelib.solve.MazeSolveAlgo cimport MazeSolveAlgo


cdef class RandomMouse(MazeSolveAlgo):
    cdef readonly bint prune


    @cython.locals(current=tuple, solution=list, ns=list, nxt=tuple)
    cpdef list _solve(self)


    @cython.locals(i=cython.int)
    cdef inline list _fix_entrances(self, list solution)
