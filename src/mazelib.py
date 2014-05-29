
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
        self.solutions = None

    def generate(self):
        if self.generator == None:
            raise UnboundLocalError('No maze-generation algorithm has been set.')
        else:
            self.grid = self.generator.generate()
            self.start = None
            self.end = None
            self.solutions = None

    def generate_entrances(self, outer=True):
        """ Generate maze entrances.

        By default, the entrances will be on opposite outer walls.
        """
        if outer:
            return self._generate_outer_entrances()
        else:
            return self._generate_inner_entrances()
        self.solutions = None

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
        while end == self.start:
            end = (randrange(1, H, 2), randrange(1, W, 2))

        self.end = end

    def generate_monte_carlo(self, repeat, entrances=3, difficulty=1.0):
        """Use the Monte Carlo Method to generate a maze of defined difficulty.

        This method assumes the generator and solver algorithms are already set.

        1. Generate a maze.
        2. For each maze, generate a series of entrances.
        3. To elliminate boring entrance choices, select only the entrances
            that yield the longest solution to a given maze.
        4. Repeat steps 1 through 3 for several mazes.
        5. Order the mazes based on the length of their maximal solutions.
        6. Based on the 'difficulty' parameter, select one of the mazes.
        """
        if difficulty < 0.0 or difficulty > 1.0:
            raise ValueError('Maze difficulty must be set from 0 to 1.')

        # generate different mazes
        mazes = []
        for i in xrange(repeat):
            self.generate()
            this_maze = []

            # for each maze, generate different entrances, and solve
            for j in xrange(entrances):
                self.generate_entrances()
                self.solve()
                length = len(self.solutions[0])
                this_maze.append({'grid': self.grid,
                                  'start': self.start,
                                  'end': self.end,
                                  'solutions': self.solutions})

            # for each maze, find the longest solution
            mazes.append(max(this_maze, key=lambda k: len(k['solutions'])))

        # sort the mazes by the length of their solution
        mazes = sorted(mazes, key=lambda k: len(k['solutions'][0]))

        # based on optional parameter, choose the maze of the currect difficulty
        posi = int((len(mazes) - 1) * difficulty)

        # save final results of Monte Carlo Simulations to this object
        self.grid = mazes[posi]['grid']
        self.start = mazes[posi]['start']
        self.end = mazes[posi]['end']
        self.solutions = mazes[posi]['solutions']

    def solve(self):
        if self.generator == None:
            raise UnboundLocalError('No maze-solving algorithm has been set.')
        elif self.start == None or self.end == None:
            raise UnboundLocalError('Start and end times must be set first.')
        else:
            self.solutions = self.solver.solve(self.grid, self.start, self.end)

    def tostring(self, entrances=False, solutions=False):
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
        if solutions and self.solutions:
            for posi in self.solutions[0]:
                r,c = posi
                txt[r] = txt[r][:c] + '+' + txt[r][c+1:]

        return '\n'.join(txt)

    def __str__(self):
        # print maze walls, entrances, and solutions, IF available
        self.tostring(True, True)

    def __repr__(self):
        return self.__str__()
