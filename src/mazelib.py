
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
        if self.generator == None:
            raise UnboundLocalError('No maze-generation algorithm has been set.')
        else:
            self.grid = self.generator.generate()

    def generate_entrances(self, outer=True):
        """ Generate maze entrances.

        By default, the entrances will be on opposite outer walls.
        """
        if outer:
            return self._generate_outer_entrances()
        else:
            return self._generate_inner_entrances()

    def _generate_outer_entrances(self):
        """ Generate maze entrances, along the outer walls. """
        H = self.grid.height
        W = self.grid.width

        start_side = randrange(4)

        # maze entrances will be on opposite sides of the maze.
        if start_side == 0:
            self.start = (0, randrange(1, W, 2)) # North
            self.end = (H - 1, randrange(1, W, 2))
        elif start_side == 1:
            self.start = (H - 1, randrange(1, W, 2)) # South
            self.end = (0, randrange(1, W, 2))
        elif start_side == 2:
            self.start = (randrange(1, H, 2), 0) # West
            self.end = (randrange(1, H, 2), W - 1)
        else:
            self.start = (randrange(1, H, 2), W - 1) # East
            self.end = (randrange(1, H, 2), 0)


    def _generate_inner_entrances(self):
        """ Generate maze entrances, randomly within the maze. """
        H = self.grid.height
        W = self.grid.width

        self.start = (randrange(1, H, 2), randrange(1, W, 2))
        end = (randrange(1, H, 2), randrange(1, W, 2))

        # make certain the start and end points aren't the same
        while end == start:
            end = (randrange(1, H, 2), randrange(1, W, 2))

        self.end = end

    def solve(self):
        if self.generator == None:
            raise UnboundLocalError('No maze-solving algorithm has been set.')
        else:
            self.solution = self.solver.solve(self.grid, self.start, self.end)

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
