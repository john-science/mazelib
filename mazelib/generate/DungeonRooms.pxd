
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
    cdef _choose_start(self)
