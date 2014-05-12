
import abc
from random import choice,random,randrange,shuffle


class Maze(object):

    def __init__(self):
        # TODO: Consider allowing grid/solution to be passed as optional parameters to Maze.
        self.generator = None
        self.grid = None
        self.start = None
        self.end = None
        self.solver = None
        self.solution = None

    def generate(self):
        self.grid = self.generator.generate()

    def generate_entrances(self):
        # TODO: The entrances should have the option of being in three places: on the edges, just inside the edges, and randomly anywhere in the maze.
        H = self.grid.height
        W = self.grid.width

        start_side = randrange(4)

        if start_side == 0:
            self.start = (0, randrange(1, W, 2))         # North
            self.end = (H - 1, randrange(1, W, 2))
        elif start_side == 1:
            self.start = (H - 1, randrange(1, W, 2))  # South
            self.end = (0, randrange(1, W, 2))
        elif start_side == 2:
            self.start = (randrange(1, H, 2), 0)          # West
            self.end = (randrange(1, H, 2), W - 1)
        else:
            self.start = (randrange(1, H, 2), W - 1)   # East
            self.end = (randrange(1, H, 2), 0)

    def solve(self):
        raise NotImplementedError('Please implement this method.')

    def tostring(self, entrances=False, solution=False):
        """Return a string representation of the maze."""
        
        # Build the walls of the grid
        txt = []
        for row in self.grid:
            txt_row = ''
            for cell in row:
                txt_row += '#' if cell else ' '
            txt.append(txt_row)
        
        # insert the start and end points
        if entrances and self.start and self.end:
            r,c = self.start
            txt[r] = txt[r][:c] + 'S' + txt[r][c+1:]
            r,c = self.end
            txt[r] = txt[r][:c] + 'E' + txt[r][c+1:]

        # if extant, insert the solution path
        if solution and self.solution:
            # TODO: Fill this in, after solve method is implemented.
            pass

        return '\n'.join(txt)

    def __str__(self):
        # print maze walls, entrances, and solutions, IF available
        self.tostring(True, True)

    def __repr__(self):
        return self.__str__()
