
from __future__ import absolute_import
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo, i8


cdef class Ellers(MazeGenAlgo):

    # attributes
    cdef float xbias
    cdef float ybias

    # functions
    cpdef i8[:,:] generate(self)
    cdef int _init_row(self, int[:,:] sets, int row, int max_set_number)
    cdef void _merge_one_row(self, int[:,:] sets, int r)
    cdef void _merge_down_a_row(self, int[:,:] sets, int start_row)
    cdef void _merge_sets(self, int[:,:] sets, int from_set, int to_set, int max_row=?)
    cdef void _process_last_row(self, int[:,:] sets)
    cdef i8[:,:] _create_grid_from_sets(self, int[:,:] sets)
