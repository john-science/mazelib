
from random import choice,randrange,shuffle


class Maze(object):

    def __init__(self):
        # TODO: Consider allowing these passed as optional parameters to Maze.
        self.grid = None
        self.generator = None
        self.solver = None

    def generate(self, rows, cols):
        pass

    def generate_entrances(self):
        pass

    def solve(self):
        pass
