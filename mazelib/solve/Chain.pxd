cimport cython
from mazelib.solve.MazeSolveAlgo cimport MazeSolveAlgo


cdef class Chain(MazeSolveAlgo):
    cdef readonly list directions


    @cython.locals(guiding_line=list, current=cython.int, solution=list, len_guiding_line=cython.int,
                   current=cython.int, success=bint)
    cpdef list _solve(self)


    @cython.locals(ns=list, robot_path=list, robot_paths=list, n=tuple, j=cython.int, path=list,
                   last_diff=tuple, last_dir=int, shortest_robot_path=list, min_len=cython.int)
    cdef inline cython.int _send_out_robots(self, list solution, list guiding_line, cython.int i)


    @cython.locals(path=list, ns=list, nxt=tuple)
    cdef inline list _backtracking_solve(self, list solution, tuple goal)


    @cython.locals(r=cython.int, c=cython.int, next=tuple, rdiff=cython.int, cdiff=cython.int)
    cdef inline bint _try_direct_move(self, list solution, list guiding_line, cython.int i)


    @cython.locals(r1=cython.int, c1=cython.int, r2=cython.int, c2=cython.int, path=list, current=tuple,
                   rdiff=cython.int, cdiff=cython.int)
    cdef inline list _draw_guiding_line(self)