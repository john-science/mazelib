cimport cython
from mazelib.transmute.MazeTransmuteAlgo cimport MazeTransmuteAlgo


cdef class CuldeSacFiller(MazeTransmuteAlgo):


    @cython.locals(r=cython.int, c=cython.int, ns=list, end1=tuple, end2=tuple)
    cpdef void _transmute(self)


    @cython.locals(first=tuple, previous=tuple, current=tuple, ns=list)
    cdef inline tuple _find_next_intersection(self, list path_start)
