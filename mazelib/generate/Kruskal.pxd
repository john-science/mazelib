
from __future__ import absolute_import
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo, i8


cdef class Kruskal(MazeGenAlgo):

    # methods
    cpdef i8[:,:] generate(self)
