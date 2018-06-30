cimport cython
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo
from numpy cimport ndarray
cimport numpy as np

cdef public cython.int SERPENTINE = 1
cdef public cython.int SPIRAL = 2


cdef class TrivialMaze(MazeGenAlgo):
    cdef readonly cython.int maze_type

    @cython.locals(grid=ndarray)
    cpdef ndarray[cython.char, ndim=2] generate(self)

    @cython.locals(vertical_skew=cython.int, row=cython.int, col=cython.int, height=cython.int, width=cython.int)
    cdef inline ndarray[cython.char, ndim=2] _generate_serpentine_maze(self, ndarray[cython.char, ndim=2] grid)

    @cython.locals(clockwise=cython.int, directions=list, current=tuple, next_dir=cython.int, next_cell=tuple,
                   ns=list)
    cdef inline ndarray[cython.char, ndim=2] _generate_spiral_maze(self, ndarray[cython.char, ndim=2] grid)

    cdef inline tuple _midpoint(self, tuple a, tuple b)

    cdef inline tuple _move(self, tuple start, tuple direction)
