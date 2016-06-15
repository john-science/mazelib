

cdef class BinaryTree(MazeGenAlgo):

    # attributes
    cdef object bias

    # methods
    cpdef i8[:,:] generate(self)
    cdef tuple _find_neighbor(self, int current_row, int current_col)
