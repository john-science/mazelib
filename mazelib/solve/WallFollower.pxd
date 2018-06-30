cimport cython
from mazelib.solve.MazeSolveAlgo cimport MazeSolveAlgo


cdef class WallFollower(MazeSolveAlgo):
    cdef readonly list directions
    cdef readonly bint prune

    @cython.locals(solution=list, current=tuple, last=tuple, last_diff=tuple, last_dir=cython.int)
    cpdef list _solve(self)

    @cython.locals(limt=cython.uint, temp=tuple, midpoint=tuple)
    cdef inline list _follow_walls(self, cython.int last_dir, tuple current, list solution)

    @cython.locals(d=cython.uint, next_dir=cython.int, next_cell=tuple, mid=tuple, r=cython.int, c=cython.int)
    cdef inline tuple _follow_one_step(self, cython.int last_dir, tuple current)

    @cython.locals(i=cython.uint)
    cdef list _fix_entrances(self, list solution)
