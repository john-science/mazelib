cimport cython
from mazelib.solve.MazeSolveAlgo cimport MazeSolveAlgo
from mazelib.solve.DeadEndFiller cimport DeadEndFiller
from mazelib.solve.ShortestPaths cimport ShortestPaths


cdef class CuldeSacFiller(MazeSolveAlgo):
    cdef readonly MazeSolveAlgo solver


    cpdef list _solve(self)


    @cython.locals(walls=list, wall=list, border=list)
    cdef inline void _seal_culdesacs(self)


    @cython.locals(N=cython.int, i=cython.int, j=cython.int)
    cdef inline list _reduce_wall_systems(self, list walls)


    @cython.locals(cell1=tuple, cell2=tuple)
    cdef inline bint _walls_are_connected(self, list wall1, list wall2)


    cdef inline list _build_solutions(self)


    cdef inline void _fix_culdesac(self, list border)


    @cython.locals(num_entrances=cython.int, cell=tuple, num_neighbors=cython.int)
    cdef inline bint _wall_is_culdesac(self, list border)


    @cython.locals(cell=tuple, r=cython.int, c=cython.int, rdiff=cython.int, cdiff=cython.int, b=tuple, border=list)
    cdef inline list _find_bordering_cells(self, list wall)


    @cython.locals(new_border=list, found=bint, cell=tuple)
    cdef inline list _remove_internal_deadends(self, list border)


    @cython.locals(new_walls=list, on_edge=bint, wall=list)
    cdef inline list _remove_border_walls(self, list walls)


    @cython.locals(walls=list, r=cython.int, c=cython.int, found=bint, i=cython.int)
    cdef inline list _find_wall_systems(self)


    @cython.locals(r_diff=cython.int, c_diff=cython.int)
    cdef inline bint _is_neighbor(self, tuple cell1, tuple cell2)


    @cython.locals(target=tuple)
    cdef inline bint _has_neighbor(self, tuple cell, list list_cells)
