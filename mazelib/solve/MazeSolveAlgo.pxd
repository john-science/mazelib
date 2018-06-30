cimport cython
from numpy cimport ndarray


cdef class MazeSolveAlgo:
    #cdef public ndarray_grid grid
    #cdef public ndarray[cython.char, ndim=2] grid
    cdef public ndarray grid
    cdef public tuple start  # TODO: Would start/end be faster as size-2 arrays?
    cdef public tuple end


    cpdef list solve(self, ndarray[cython.char, ndim=2] grid, tuple start, tuple end)


    cdef inline void _solve_preprocessor(self, ndarray[cython.char, ndim=2] grid, tuple start, tuple end)  # TODO: needs expect -1


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


    @cython.locals(found=bint, attempt=cython.int, first_i=cython.int, last_i=cython.int, i=cython.int,
                   max_attempt=cython.int, first=tuple)
    cpdef list _prune_solution(self, list solution)
