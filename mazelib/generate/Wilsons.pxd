
from __future__ import absolute_import
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo, i8


cdef class Wilsons(MazeGenAlgo):

    # attributes
    cdef object _hunt_order

    # methods
    cpdef i8[:,:] generate(self)
    cdef tuple _random_dir(self, tuple current)
    cdef tuple _move(self, tuple start, tuple direction)
