
from __future__ import absolute_import
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo, i8


cdef class Perturbation(MazeGenAlgo):

    # attributes
    cdef i8[:,:] grid
    cdef int repeat
    cdef int new_walls

    # methods
    cpdef i8[:,:] generate(self)
