
from __future__ import absolute_import
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo, i8


cdef class BinaryTree(MazeGenAlgo):

    # attributes
    cdef object bias

    # methods
    cpdef i8[:,:] generate(self)
    cdef tuple _find_neighbor(self, int current_row, int current_col)
