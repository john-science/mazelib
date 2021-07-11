cimport cython
from mazelib.solve.MazeSolveAlgo cimport MazeSolveAlgo


cdef class ShortestPath(MazeSolveAlgo):
    cdef readonly bint start_edge
    cdef readonly bint end_edge


    @cython.locals(start=tuple, start_posis=list, solutions=list, s=tuple, num_unfinished=cython.int,
                   ns=list, s=cython.int, sp=tuple, j=cython.int, nxt=list)
    cpdef list _solve(self)


    @cython.locals(new_solutions=list, sol=list, new_sol=list, last=tuple)
    cdef inline list _clean_up(self, list solutions)


    @cython.locals(s=tuple)
    cdef inline list _remove_duplicate_sols(self, list sols)
