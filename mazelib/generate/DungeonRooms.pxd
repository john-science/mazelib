
from __future__ import absolute_import
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo, i8


cdef class DungeonRooms(MazeGenAlgo):

    # attributes
    cdef object rooms
    cdef i8[:,:] grid
    cdef i8[:,:] backup_grid
    cdef object _hunt_order

    # methods
    cpdef i8[:,:] generate(self)
    cdef void _carve_rooms(self, rooms)
    cdef void _carve_room(self, top_left, bottom_right)
    cdef void _carve_door(self, top_left, bottom_right)
    cdef _choose_start(self)
    cdef void _walk(self, start)
    cdef void _reconnect_maze(self)
    cdef void _fix_disjoint_passages(self, disjoint_passages)
