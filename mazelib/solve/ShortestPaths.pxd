cimport cython
#cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
from mazelib.solve.MazeSolveAlgo cimport MazeSolveAlgo


cdef class ShortestPaths(MazeSolveAlgo):
    cdef readonly bint start_edge
    cdef readonly bint end_edge


    @cython.locals(start=tuple, start_posis=tuple, solutions=list, s=tuple, num_unfinished=cython.int,
                   ns=list, s=tuple, j=cython.int, nxt=list)
    cpdef list _solve(self)


    @cython.locals(new_solutions=list, sol=list, new_sol=list, last=tuple)
    cdef inline list _clean_up(self, list solutions)


    @cython.locals(found=bint, i=cython.int, diff=cython.int, index=cython.int, ind=cython.int)
    cpdef list _prune_solution(self, list sol)


    @cython.locals(temp=list, s=tuple)
    cdef inline list _remove_duplicate_sols(self, list sols)
