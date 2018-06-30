cimport cython
from mazelib.solve.MazeSolveAlgo cimport MazeSolveAlgo

cdef tuple END = (-999, -9)
cdef tuple DEAD_END = (-9, -999)


cdef class Collision(MazeSolveAlgo):

    @cython.locals(start=tuple, paths=list, temp_paths=list, diff=list)
    cpdef list _solve(self)

    @cython.locals(paths=list, temp_paths=list)
    cdef inline list _flood_maze(self, tuple start)

    @cython.locals(temp_paths=list, step_made=bint, ns=list, mid=tuple, neighbor=tuple)
    cdef inline list _one_time_step(self, list paths)

    @cython.locals(N=cython.uint, i =cython.uint, j=cython.uint, row=cython.int, col=cython.int)
    cdef inline list _fix_collisions(self, list paths)

    @cython.locals(p=list)
    cpdef list _fix_entrances(self, list paths)
