cimport cython
#cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
from numpy cimport ndarray


cdef class MazeSolveAlgo:
    cdef public ndarray grid
    cdef public ndarray start
    cdef public ndarray end

    cpdef list solve(self, ndarray grid, tuple start, tuple end)

    cdef inline void _solve_preprocessor(self, ndarray grid, tuple start, tuple end)  # TODO: needs expect -1

    cpdef list _solve(self)

    @cython.locals(r=cython.int, c=cython.int, ns=list)
    cpdef list _find_neighbors(self, tuple posi, bint is_wall=*)

    @cython.locals(r=cython.int, c=cython.int, ns=list)
    cpdef list _find_unblocked_neighbors(self, tuple posi)

    cpdef tuple _midpoint(self, tuple a, tuple b)

    cpdef tuple _move(self, tuple start, tuple direction)

    @cython.locals(r=cython.int, c=cython.int)
    cpdef bint _on_edge(self, tuple cell)

    @cython.locals(r=cython.int, c=cython.int)
    cpdef tuple _push_edge(self, tuple cell)

    cpdef bint _within_one(self, tuple cell, tuple desire)

    @cython.locals(found=bint, diff=cython.int, i=cython.uint, index=cython.uint, ind=cython.int)
    cpdef list _prune_solution(self, list solution)
