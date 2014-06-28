
from array2d import Array2D


class MazeArray(Array2D):

    def __init__(self, h, w, default_value=True):
        super(MazeArray, self).__init__('b', (h, w), default_value)
