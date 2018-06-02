cimport cython
#cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
from mazelib.solve.MazeSolveAlgo cimport MazeSolveAlgo


cdef class Collision(MazeSolveAlgo):

    @cython.locals(start=tuple, paths=list, temp_paths=list, diff=list)
    cpdef list _solve(self)

    @cython.locals(paths=list, temp_paths=list)
    cdef inline list _flood_maze(self, tuple start)  # TODO: TEST: changed to "cdef", if works, add "inline"

    @cython.locals(temp_paths=list, step_made=bint, ns=list, mid=tuple, neighbor=tuple)
    cdef inline list _one_time_step(self, list paths)

    @cython.locals(N=cython.uint, i =cython.uint, j=cython.uint)
    cdef inline list _fix_collisions(self, list paths)

    cpdef list _fix_entrances(self, list paths)
