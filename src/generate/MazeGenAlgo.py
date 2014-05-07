
import abc


class MazeGenAlgo(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, h, w):
        if w < 2 or h < 2:
            raise ValueError('The width and height of a maze have to be greater than one.')
        self.h = h
        self.w = w
        self.H = (2 * self.h) + 1
        self.W = (2 * self.w) + 1
    
    @abc.abstractmethod
    def generate(self):
        return
