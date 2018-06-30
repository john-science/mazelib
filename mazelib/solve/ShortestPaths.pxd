cimport cython
from mazelib.solve.MazeSolveAlgo cimport MazeSolveAlgo


cdef class ShortestPaths(MazeSolveAlgo):
    cdef readonly bint start_edge
    cdef readonly bint end_edge


    @cython.locals(start=tuple, start_posis=list, solutions=list, s=cython.int, num_unfinished=cython.int,
                   ns=list, j=cython.int, nxt=list, sp=tuple)
    cpdef list _solve(self)


    @cython.locals(new_solutions=list, sol=list, new_sol=list, last=tuple)
    cdef inline list _clean_up(self, list solutions)


    @cython.locals(found=bint, i=cython.int, diff=cython.int, index=cython.int, ind=cython.int)
    cpdef list _prune_solution(self, list sol)


    @cython.locals(s=tuple)
    cdef inline list _remove_duplicate_sols(self, list sols)
