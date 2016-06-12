

cdef class MazeGenAlgo:

    # class attributes
    cdef public int h
    cdef public int w
    cdef public int H
    cdef public int W

    # functions
    cpdef object generate(self)
    cpdef object _find_neighbors(self, posi, grid, is_wall=?)
