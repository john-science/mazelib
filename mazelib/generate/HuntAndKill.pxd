
from __future__ import absolute_import
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo, i8


cdef class HuntAndKill(MazeGenAlgo):

    # attributes
    cdef object _hunt_order

    # methods
    cpdef i8[:,:] generate(self)
    cdef void _walk(self, i8 [:,:] grid, int row, int col)
