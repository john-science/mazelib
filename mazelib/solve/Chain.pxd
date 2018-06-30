cimport cython
from mazelib.solve.MazeSolveAlgo cimport MazeSolveAlgo


cdef class Chain(MazeSolveAlgo):
    cdef readonly list directions
    cdef readonly bint prune


    @cython.locals(guiding_line=list, current=cython.int, solution=list, len_guiding_line=cython.int,
                   current=cython.int, success=bint)
    cpdef list _solve(self)


    #@cython.locals(ns=list, robot_path=list, robot_paths=list, n=tuple, j=cython.int, path=list,
    #               last_diff=tuple, last_dir=int, shortest_robot_path=list, min_len=cython.int)
    cdef inline cython.int _send_out_robots(self, list solution, list guiding_line, cython.int i) except -999


    @cython.locals(last_diff=tuple, last_dir=cython.int)
    cdef inline bint _has_robot_returned(self, cython.int first_dir, list path)


    @cython.locals(path=list, first_diff=tuple, first_dir=cython.int, temp=tuple)
    cdef inline list _follow_walls(self, cython.int last_dir, tuple current, list solution, list goal)


    @cython.locals(d=cython.int, next_dir=cython.int, next_cell=tuple, r=cython.int, c=cython.int)
    cdef inline tuple _follow_one_step(self, cython.int last_dir, tuple current)


    @cython.locals(r=cython.int, c=cython.int, next=tuple, rdiff=cython.int, cdiff=cython.int)
    cdef inline bint _try_direct_move(self, list solution, list guiding_line, cython.int i)


    @cython.locals(r1=cython.int, c1=cython.int, r2=cython.int, c2=cython.int, path=list, current=tuple,
                   rdiff=cython.int, cdiff=cython.int)
    cdef inline list _draw_guiding_line(self)


    @cython.locals(i=cython.int)
    cdef inline list _fix_entrances(self, list solution)
