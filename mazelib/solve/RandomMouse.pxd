from random import choice, shuffle
cimport cython
from mazelib.solve.MazeSolveAlgo cimport MazeSolveAlgo


cdef class RandomMouse(MazeSolveAlgo):


    @cython.locals(current=tuple, solution=list, ns=list, nxt=tuple)
    cpdef list _solve(self)
