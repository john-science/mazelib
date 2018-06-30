cimport cython
from mazelib.solve.MazeSolveAlgo cimport MazeSolveAlgo


cdef class Tremaux(MazeSolveAlgo):
    cdef readonly dict visited_coords


    @cython.locals(solution=list, current=tuple, ns=list, nxt=tuple)
    cpdef list _solve(self)


    cdef inline void _visit(self, tuple cell)


    cdef inline cython.int _get_visit_count(self, tuple cell)


    @cython.locals(i=cython.int)
    cdef inline list _fix_entrances(self, list solution)
