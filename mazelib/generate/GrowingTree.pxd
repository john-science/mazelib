
from __future__ import absolute_import
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo, i8


cdef class GrowingTree(MazeGenAlgo):

    # attributes
    cdef public float backtrack_chance

    # methods
    cpdef i8[:,:] generate(self)
