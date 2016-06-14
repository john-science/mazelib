
import cython
cimport numpy as cnp
cnp.import_array()

ctypedef cnp.int8_t i8


cdef class MazeGenAlgo:

    # class attributes
    cdef public int h
    cdef public int w
    cdef public int H
    cdef public int W

    # functions
    cpdef i8[:,:] generate(self)
    cpdef object _find_neighbors(self, posi, grid, is_wall=?)
