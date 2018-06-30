cimport cython
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo
from numpy cimport ndarray
cimport numpy as np


cdef class Ellers(MazeGenAlgo):
    cdef readonly double xskew
    cdef readonly double yskew

    @cython.locals(grid=ndarray, sets=ndarray, max_set_number=cython.int, r=cython.int)
    cpdef ndarray[cython.char, ndim=2] generate(self)

    @cython.locals(c=cython.int, max_set_number=cython.int)
    cdef inline cython.int _init_row(self, ndarray[cython.char, ndim=2] sets, cython.int row, cython.int max_set_number)

    @cython.locals(c=cython.int)
    cdef inline void _merge_one_row(self, ndarray[cython.char, ndim=2] sets, cython.int r)

    @cython.locals(set_counts=dict, c=cython.int, s=cython.int)
    cdef inline void _merge_down_a_row(self, ndarray[cython.char, ndim=2] sets, cython.int start_row)

    @cython.locals(c=cython.int, r=cython.int)
    cdef inline void _merge_sets(self, ndarray[cython.char, ndim=2] sets, cython.int from_set, cython.int to_set, cython.int max_row=*)

    @cython.locals(c=cython.int, r=cython.int)
    cdef inline void _process_last_row(self, ndarray[cython.char, ndim=2] sets)

    @cython.locals(grid=ndarray, c=cython.int, r=cython.int)
    cdef inline ndarray[cython.char, ndim=2] _create_grid_from_sets(self, ndarray[cython.char, ndim=2] sets)
