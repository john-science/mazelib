
from random import randrange,shuffle
from MazeGenAlgo import MazeGenAlgo
from MazeArray import MazeArray


class Backtrack(MazeGenAlgo):

    def __init__(self, w, h):
        super(Backtrack, self).__init__(w, h)

    def generate(self):
        """
        Choose a starting point in the field.
        Randomly choose a wall at that point and carve a passage
            through to the adjacent cell, but only if the adjacent
            cell has not been visited yet. This becomes the new current cell.
        If all adjacent cells have been visited, back up to the
            last cell that has uncarved walls and repeat.
        The algorithm ends when the process has backed all the way up
            to the starting point.
        """

        grid = MazeArray(self.H, self.W)

        raise NotImplementedError('Algorithm not yet implemented.')

        return grid
