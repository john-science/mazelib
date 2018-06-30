cimport cython
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo
from numpy cimport ndarray
cimport numpy as np


cdef class Perturbation(MazeGenAlgo):
    cdef public ndarray grid
    cdef readonly cython.uint repeat
    cdef readonly cython.uint new_walls


    @cython.locals(grid=ndarray, i=cython.int, j=cython.int)
    cpdef ndarray[cython.char, ndim=2] generate(self)


    @cython.locals(limit=cython.int, tries=cython.int, found=bint, row=cython.int, col=cython.int)
    cdef inline ndarray[cython.char, ndim=2] _add_a_random_wall(self, ndarray[cython.char, ndim=2] grid)


    @cython.locals(passages=list)
    cdef inline ndarray[cython.char, ndim=2] _reconnect_maze(self, ndarray[cython.char, ndim=2] grid)


    @cython.locals(passages=list, found=bint, r=cython.int, c=cython.int, ns=list, current=set, i=cython.int,
                   passage=set, intersect=set)
    cdef inline list _find_all_passages(self, ndarray[cython.char, ndim=2] grid)


    @cython.locals(found=bint, cell=tuple, neighbors=list, passage=set, intersect=list, c=tuple, cell=tuple,
                   mid=tuple)
    cdef inline ndarray[cython.char, ndim=2] _fix_disjoint_passages(self, list disjoint_passages, ndarray[cython.char, ndim=2] grid)


    @cython.locals(i=cython.int, j=cython.int, intersect=set, l=set)
    cpdef list _join_intersecting_sets(self, list list_of_sets)


    @cython.locals(r=cython.int, c=cython.int, ns=list)
    cdef inline list _find_unblocked_neighbors(self, ndarray[cython.char, ndim=2] grid, tuple posi)


    cdef inline tuple _midpoint(self, tuple a, tuple b)
