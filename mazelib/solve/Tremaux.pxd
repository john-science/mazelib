cimport cython
from mazelib.solve.MazeSolveAlgo cimport MazeSolveAlgo


cdef class Tremaux(MazeSolveAlgo):
    cdef readonly dict visited_cells


    @cython.locals(solution=list, ns=list, current=tuple, nxt=tuple)
    cpdef list _solve(self)


    cdef inline void _visit(self, tuple cell)


    cdef inline cython.int _get_visit_count(self, tuple cell)


    @cython.locals(visit_counts=dict, neighbor=tuple, visit_count=int)
    cdef inline tuple _what_next(self, list ns, list solution)
