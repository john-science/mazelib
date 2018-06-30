from random import choice, shuffle
cimport cython
from mazelib.solve.MazeSolveAlgo cimport MazeSolveAlgo


cdef class RandomMouse(MazeSolveAlgo):
    cdef readonly bint prune


    @cython.locals(current=tuple, solution=list, ns=list, nxt=tuple)
    cpdef list _solve(self)


    @cython.locals(d=cython.int, next_dir=cython.int, next_cell=tuple, r=cython.int, c=cython.int)
    cdef inline tuple _move_to_next_cell(self, cython.int last_dir, tuple current)


    @cython.locals(i=cython.int)
    cdef inline list _fix_entrances(self, list solution)
