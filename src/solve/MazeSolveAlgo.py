
import abc
from ..utils.MazeArray import MazeArray


class MazeSolveAlgo(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, grid, start, stop):
        self.grid = grid
        self.start = start
        self.end = end

    @abc.abstractmethod
    def solve(self):
        return
