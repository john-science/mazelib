
import abc


class MazeSolveAlgo(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def solve(self, grid, start, end):
        return
