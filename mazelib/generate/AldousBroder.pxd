
from __future__ import absolute_import
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo, i8


cdef class AldousBroder(MazeGenAlgo):

    cpdef i8[:,:] generate(self)
