
import abc
import numpy as np
from numpy.random import shuffle


class MazeGenAlgo: 
    __metaclass__ = abc.ABCMeta

    def __init__(self, h, w):
        if w < 3 or h < 3:
            raise ValueError('Mazes cannot be smaller than 3x3.')
        self.h = h
        self.w = w
        self.H = (2 * self.h) + 1
        self.W = (2 * self.w) + 1

    @abc.abstractmethod
    def generate(self):
        return None 
 
    """ All of the methods below this are helper methods,
        common to many maze-generating algorithms.
    """

    def _find_neighbors(self, r, c, grid, is_wall=False):
        """ Find all the grid neighbors of the current position;
            visited, or not.
        """
        ns = []

        if r > 1 and grid[r-2][c] == is_wall:
            ns.append((r-2, c))
        if r < self.H-2 and grid[r+2][c] == is_wall:
            ns.append((r+2, c))
        if c > 1 and grid[r][c-2] == is_wall:
            ns.append((r, c-2))
        if c < self.W-2 and grid[r][c+2] == is_wall:
            ns.append((r, c+2))

        shuffle(ns)

        return ns
