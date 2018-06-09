cimport cython
#cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
from mazelib.generate.MazeGenAlgo cimport MazeGenAlgo
from numpy cimport ndarray
cimport numpy as np


cdef class Kruskal(MazeGenAlgo):

    @cython.locals(grid=ndarray, row=cython.int, col=cython.int, forest=list, edges=list, new_tree=list,
                   ce_row=cython.int, ce_col=cython.int, tree1=cython.int, tree2=cython.int,
                   temp1=list, temp2=list)
    cpdef ndarray[cython.char, ndim=2] generate(self)
