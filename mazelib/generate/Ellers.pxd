
from __future__ import absolute_import
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo


cdef class Ellers(MazeGenAlgo):

    # attributes
    cdef float xbias
    cdef float ybias

    # functions
    cpdef generate(self)
    cdef _init_row(self, int[:,:] sets, int row, int max_set_number)
    cdef _merge_one_row(self, int[:,:] sets, int r)
    cdef _merge_down_a_row(self, int[:,:] sets, int start_row)
    cdef _merge_sets(self, int[:,:] sets, int from_set, int to_set, int max_row=?)
    cdef _process_last_row(self, int[:,:] sets)
    cdef _create_grid_from_sets(self, int[:,:] sets)
