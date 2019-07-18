cimport cython
from mazelib.simplify.MazeSimplifyAlgo cimport MazeSimplifyAlgo


cdef class CuldeSacFiller(MazeSimplifyAlgo):


    @cython.locals(r=cython.int, c=cython.int, ns=list, end1=tuple, end2=tuple)
    cpdef void _simplify(self)


    @cython.locals(first=tuple, previous=tuple, current=tuple, ns=list)
    cdef inline tuple _find_next_intersection(self, list path_start)
