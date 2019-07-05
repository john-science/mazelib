
from random import choice, randrange
import numpy as np
# If the code is not Cython-compiled, we need to add some imports.
try:
    from cython import compiled
except ModuleNotFoundError:
    compiled = False
if not compiled:
    from mazelib.generate.MazeGenAlgo import MazeGenAlgo

RANDOM = 1
SERPENTINE = 2


class Wilsons(MazeGenAlgo):
    """ The Algorithm

    1. Choose a random cell and add it to the Uniform Spanning Tree (UST).
    2. Select any cell that is not in the UST and perform a random walk until you find a cell that is.
    3. Add the cells and walls visited in the random walk to the UST.
    4. Repeat steps 2 and 3 until all cells have been added to the UST.
    """

    def __init__(self, w, h, hunt_order='random'):
        super(Wilsons, self).__init__(w, h)

        # the user can define what order to hunt for the next cell in
        if hunt_order.lower().strip() == 'serpentine':
            self._hunt_order = SERPENTINE
        else:
            self._hunt_order = RANDOM

    def generate(self):
        # create empty grid
        grid = np.empty((self.H, self.W), dtype=np.int8)
        grid.fill(1)

        # find an arbitrary starting position
        grid[randrange(1, self.H, 2)][randrange(1, self.W, 2)] = 0
        num_visited = 1
        row, col = self._hunt(grid, num_visited)

        # perform many random walks, to fill the maze
        while row != -1 and col != -1:
            walk = self._generate_random_walk(grid, (row, col))
            num_visited += self._solve_random_walk(grid, walk, (row, col))
            (row, col) = self._hunt(grid, num_visited)

        return grid

    def _hunt(self, grid, count):
        """ Based on how this algorithm was configured, choose hunt for the next starting point.
        """
        if self._hunt_order == SERPENTINE:
            return self._hunt_serpentine(grid, count)
        else:
            return self._hunt_random(grid, count)

    def _hunt_random(self, grid, count):
        """ Select the next cell to walk from, randomly. """
        if count >= (self.h * self.w):
            return (-1, -1)

        return (randrange(1, self.H, 2), randrange(1, self.W, 2))

    def _hunt_serpentine(self, grid, count):
        """ Select the next cell to walk from by cycling through every grid cell in order.
        """
        cell = (1, -1)
        found = False

        while not found:
            cell = (cell[0], cell[1] + 2)
            if cell[1] > (self.W - 2):
                cell = (cell[0] + 2, 1)
                if cell[0] > (self.H - 2):
                    return (-1, -1)

            if grid[cell[0]][cell[1]] != 0:
                found = True

        return cell

    def _generate_random_walk(self, grid, start):
        """ From a given starting position,
        walk randomly until you hit a visited cell.

        The returned walk object is a dictionary mapping your location (cell) to a
        direction. If you randomly walk over the same cell twice, you overwrite
        the direction at that location.
        """
        direction = self._random_dir(start)
        walk = {}
        walk[start] = direction
        current = self._move(start, direction)

        while grid[current[0]][current[1]] == 1:
            direction = self._random_dir(current)
            walk[current] = direction
            current = self._move(current, direction)

        return walk

    def _random_dir(self, current):
        """ Take a step on one random (but valid) direction """
        r,c = current
        options = []
        if r > 1:            options.append(0)  # North
        if r < (self.H - 2): options.append(1)  # South
        if c > 1:            options.append(2)  # East
        if c < (self.W - 2): options.append(3)  # West

        direction = choice(options)
        if direction == 0:   return (-2, 0)  # North
        elif direction == 1: return (2, 0)   # South
        elif direction == 2: return (0, -2)  # East
        else:                return (0, 2)   # West

    def _move(self, start, direction):
        """ Convolve a position tuple with a direction tuple to generate a new position.
        """
        return (start[0] + direction[0], start[1] + direction[1])

    def _solve_random_walk(self, grid, walk, start):
        """ Move through the random walk, visiting all the cells you touch,
        and breaking down the walls you cross.
        """
        visits = 0
        current = start

        while grid[current[0]][current[1]] != 0:
            grid[current] = 0
            next1 = self._move(current, walk[current])
            grid[(next1[0] + current[0]) // 2, (next1[1] + current[1]) // 2] = 0
            visits += 1
            current = next1

        return visits
