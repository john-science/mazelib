cimport cython
from mazelib.solve.MazeSolveAlgo cimport MazeSolveAlgo
from mazelib.solve.ShortestPaths cimport ShortestPaths

cpdef public cython.int FILLER = 1
cpdef public cython.int SEALER = 2


cdef class BlindAlley(MazeSolveAlgo):
    cdef public MazeSolveAlgo solver
    cdef public cython.int _remove_dead_end


    cpdef list _solve(self)


    @cython.locals(walls=list, border=list)
    cdef inline void _seal_culdesacs(self)


    @cython.locals(N=cython.int, i=cython.int, j=cython.int)
    cdef inline list _reduce_wall_systems(self, list walls)


    @cython.locals(cell1=tuple, cell2=tuple)
    cdef inline bint _walls_are_connected(self, list wall1, list wall2)


    cdef inline list _build_solutions(self)


    @cython.locals(r=cython.int, c=cython.int)
    cdef inline void _fix_culdesac(self, list border)


    @cython.locals(num_entrances=cython.int, num_neighbors=cython.int, cell=tuple)
    cdef inline bint _wall_is_culdesac(self, list border)


    @cython.locals(border=list, r=cython.int, c=cython.int, rdiff=cython.int, cdiff=cython.int, b=tuple, cell=tuple)
    cdef inline list _find_bordering_cells(self, list wall)


    @cython.locals(found=bint, new_border=list, cell=tuple)
    cdef inline list _remove_internal_deadends(self, list border)


    @cython.locals(new_walls=list, on_edge=bint, walls=list, cell=tuple)
    cdef inline list _remove_border_walls(self, list walls)


    @cython.locals(walls=list, r=cython.int, c=cython.int, found=bint, i=cython.int)
    cdef inline list _find_wall_systems(self)


    @cython.locals(r_diff=cython.int, c_diff=cython.int)
    cdef inline bint _is_neighbor(self, tuple cell1, tuple cell2)


    @cython.locals(target=tuple)
    cdef inline bint _has_neighbor(self, tuple cell, list list_cells)


    @cython.locals(r=cython.int, c=cython.int)
    cdef inline void _fill_dead_ends(self)


    @cython.locals(r=cython.int, c=cython.int, ns=list)
    cdef inline void _dead_end_filler(self, tuple dead_end)


    @cython.locals(current=tuple, ns=list, last=tuple, r=cython.int, c=cython.int)
    cdef inline void _dead_end_sealer(self, tuple dead_end)


    @cython.locals(ns=list)
    cdef inline bint _is_dead_end(self, tuple cell)
