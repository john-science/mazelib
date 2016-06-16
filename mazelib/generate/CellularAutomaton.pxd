
from __future__ import absolute_import
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo, i8


cdef class CellularAutomaton(MazeGenAlgo):

    # attributes
    cdef float complexity
    cdef float density

    # methods
    cpdef i8[:,:] generate(self)
