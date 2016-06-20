
import cython
cimport numpy as cnp
import numpy as np
cnp.import_array()
'''
import cython
cimport numpy as cnp
cnp.import_array()
'''

ctypedef cnp.int8_t i8


cdef class MazeGenAlgo:

    # class attributes
    cdef public int h
    cdef public int w
    cdef public int H
    cdef public int W

    # functions
    cpdef i8[:,:] generate(self)
    cpdef list _find_neighbors(self, tuple posi, i8[:,:] grid, bint is_wall=?)
