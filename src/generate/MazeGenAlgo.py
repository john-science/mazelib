
import abc
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
