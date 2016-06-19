
from __future__ import absolute_import
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo, i8


cdef class TrivialMaze(MazeGenAlgo):

    # attributes
    cdef object sub_gen

    # methods
    cpdef i8[:,:] generate(self)
    cdef tuple _midpoint(self, tuple a, tuple b)
    cdef tuple _move(self, tuple start, tuple direction)
