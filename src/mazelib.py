
import abc
from random import choice,random,randrange,shuffle


class Maze(object):

    def __init__(self):
        # TODO: Consider allowing grid/solution to be passed as optional parameters to Maze.
        self.generator = None
        self.grid = None
        self.solver = None
        self.solution = None
        self.start = None
        self.end = None

    def generate(self):
        self.grid = self.generator.generate()

    def generate_random_entrances(self):
        rows = len(self.grid)
        cols = len(self.grid[0])

        start_side = randrange(4)

        if start_side == 0:
            self.start = (0, randrange(1, cols, 2))         # North
            self.end = (rows - 1, randrange(1, cols, 2))
        elif start_side == 1:
            self.start = (rows - 1, randrange(1, cols, 2))  # South
            self.end = (0, randrange(1, cols, 2))
        elif start_side == 2:
            self.start = (randrange(1, rows, 2), 0)          # West
            self.end = (randrange(1, rows, 2), cols - 1)
        else:
            self.start = (randrange(1, rows, 2), cols - 1)   # East
            self.end = (randrange(1, rows, 2), 0)

    def solve(self):
        raise NotImplementedError('Please Implement this method.')

    def tostring(self, entrances=False, solution=False):
        """Return a string representation of the maze."""
        txt = ''
        for row in self.grid:
            for cell in row:
                txt += '#' if cell else ' '
            txt += '\n'

        return txt

    def __str__(self):
        # TODO: At some ponit, this will include Entrances and solutions.
        self.tostring()

    def __repr__(self):
        return self.__str__()
