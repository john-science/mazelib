
import abc
from random import shuffle
from ..utils.MazeArray import MazeArray


class MazeGenAlgo(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, h, w):
        if w < 3 or h < 3:
            raise ValueError('A maze smaller than 3x3 is not a maze.')
        self.h = h
        self.w = w
        self.H = (2 * self.h) + 1
        self.W = (2 * self.w) + 1

    @abc.abstractmethod
    def generate(self):
        return

    def find_neighbors(self, posi, grid, visited=True):
        """Find all the grid neighbors of the current position;
        visited, or not.
        """
        (row, col) = posi
        ns = []

        if row > 1 and grid[row-2, col] != visited:
            ns.append((row-2, col))
        if row < self.H-2 and grid[row+2, col] != visited:
            ns.append((row+2, col))
        if col > 1 and grid[row, col-2] != visited:
            ns.append((row, col-2))
        if col < self.W-2 and grid[row, col+2] != visited:
            ns.append((row, col+2))

        shuffle(ns)

        return ns
