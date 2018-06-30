cimport cython
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo
from numpy cimport ndarray
cimport numpy as np

cdef public cython.int RANDOM = 1
cdef public cython.int SERPENTINE = 2


cdef class DungeonRooms(MazeGenAlgo):
    cdef public ndarray grid
    cdef readonly ndarray backup_grid
    cdef readonly list rooms
    cdef readonly cython.int _hunt_order


    @cython.locals(current=tuple, num_trials=cython.int)
    cpdef ndarray[cython.char, ndim=2] generate(self)


    cdef inline void _carve_rooms(self, list rooms)


    @cython.locals(row=cython.int, col=cython.int)
    cdef inline void _carve_room(self, tuple top_left, tuple bottom_right)


    @cython.locals(i=cython.int, even_squares=list, possible_doors=list, odd_rows=list, odd_cols=list, door=tuple)
    cpdef void _carve_door(self, tuple top_left, tuple bottom_right)


    @cython.locals(current=tuple, unvisited_neighbors=list, neighbor=tuple)
    cdef inline void _walk(self, tuple start)


    cpdef _hunt(self, int count)


    cdef inline tuple _hunt_random(self, int count)


    @cython.locals(cell=tuple, found=bint)
    cdef inline tuple _hunt_serpentine(self, int count)


    @cython.locals(current=tuple, LIMIT=cython.int, num_tries=cython.int)
    cdef inline tuple _choose_start(self)


    cdef inline void _reconnect_maze(self)


    @cython.locals(passages=list, r=cython.int, c=cython.int, ns=list, current=set, found=bint, i=cython.int,
                   intersect=set)
    cdef inline list _find_all_passages(self)


    @cython.locals(found=bint, cell=tuple, neighbors=list, passage=set, intersect=list, mid=tuple)
    cdef inline void _fix_disjoint_passages(self, list disjoint_passages)


    @cython.locals(r=cython.int, c=cython.int, ns=list)
    cdef inline list _find_unblocked_neighbors(self, tuple posi)


    @cython.locals(i=cython.int, j=cython.int, intersect=set, l=set)
    cpdef list _join_intersecting_sets(self, list list_of_sets)


    cdef inline tuple _midpoint(self, tuple a, tuple b)
