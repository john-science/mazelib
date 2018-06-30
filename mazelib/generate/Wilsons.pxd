cimport cython
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo
from numpy cimport ndarray
cimport numpy as np


cdef public cython.int RANDOM = 1
cdef public cython.int SERPENTINE = 2


cdef class Wilsons(MazeGenAlgo):
    cdef readonly cython.int _hunt_order


    @cython.locals(grid=ndarray, row=cython.int, col=cython.int, num_visited=cython.int,
                   walk=dict)
    cpdef ndarray[cython.char, ndim=2] generate(self)


    cdef inline tuple _hunt(self, ndarray[cython.char, ndim=2] grid, cython.int count)


    cdef inline tuple _hunt_random(self, ndarray[cython.char, ndim=2] grid, cython.int count)


    @cython.locals(cell=tuple, found=bint)
    cdef inline tuple _hunt_serpentine(self, ndarray[cython.char, ndim=2] grid, cython.int count)


    @cython.locals(direction=tuple, walk=dict, current=tuple)
    cdef inline dict _generate_random_walk(self, ndarray[cython.char, ndim=2] grid, tuple start)


    @cython.locals(r=cython.int, c=cython.int, options=list, direction=cython.int)
    cdef inline tuple _random_dir(self, tuple current)


    cdef inline tuple _move(self, tuple start, tuple direction)


    @cython.locals(visits=cython.int, current=tuple, next1=tuple)
    cdef inline cython.int _solve_random_walk(self, ndarray[cython.char, ndim=2] grid, dict walk, tuple start)
