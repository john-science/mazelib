cimport cython
from mazelib.transmute.MazeTransmuteAlgo cimport MazeTransmuteAlgo
from numpy cimport ndarray
cimport numpy as np


cdef class Perturbation(MazeTransmuteAlgo):
    cdef readonly cython.uint repeat
    cdef readonly cython.uint new_walls


    @cython.locals(grid=ndarray, i=cython.int, j=cython.int)
    cpdef void _transmute(self)


    @cython.locals(limit=cython.int, tries=cython.int, found=bint, row=cython.int, col=cython.int)
    cdef inline void _add_a_random_wall(self)


    @cython.locals(passages=list)
    cdef inline void _reconnect_maze(self)


    @cython.locals(passages=list, found=bint, r=cython.int, c=cython.int, ns=list, current=set,
                   i=cython.int, passage=set, intersect=set)
    cdef inline list _find_all_passages(self)


    @cython.locals(found=bint, cell=tuple, neighbors=list, passage=set, intersect=list, c=tuple,
                   cell=tuple, mid=tuple)
    cdef inline ndarray[cython.char, ndim=2] _fix_disjoint_passages(self, list disjoint_passages)


    @cython.locals(i=cython.int, j=cython.int, intersect=set, l=set)
    cpdef list _join_intersecting_sets(self, list list_of_sets)
