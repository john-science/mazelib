
from random import randint
import numpy as np
# If the code is not Cython-compiled, we need to add some imports.
from cython import compiled
if not compiled:
    from mazelib.generate.MazeGenAlgo import MazeGenAlgo

SERPENTINE = 1
SPIRAL = 2


class TrivialMaze(MazeGenAlgo):
    """
    The Algorithm

    This is actually a collection of little tools to make simple,
    unicursal mazes. Currently, there are two trivial mazes available:
    serpentine and spiral.
    """

    def __init__(self, h, w, maze_type='spiral'):
        """
        Initialize a texture.

        Args:
            self: (todo): write your description
            h: (int): write your description
            w: (int): write your description
            maze_type: (str): write your description
        """
        if maze_type.lower().strip() == 'serpentine':
            self.maze_type = SERPENTINE
        else:
            self.maze_type = SPIRAL

        super(TrivialMaze, self).__init__(h, w)

    def generate(self):
        """
        Generate a sparse matrix.

        Args:
            self: (todo): write your description
        """
        # create empty grid
        grid = np.empty((self.H, self.W), dtype=np.int8)
        grid.fill(1)

        if self.maze_type == SERPENTINE:
            return self._generate_serpentine_maze(grid)
        else:
            return self._generate_spiral_maze(grid)

    def _generate_serpentine_maze(self, grid):
        """ Create a simple maze that snakes around the grid.
        This is a unicursal maze (with no dead ends).
        """
        vertical_skew = randint(0, 1)
        height = grid.shape[0]
        width = grid.shape[1]

        if vertical_skew:
            for row in range(1, height - 1):
                for col in range(1, width - 1, 2):
                    grid[(row, col)] = 0
            # add minor passages
            for col in range(2, width - 1, 4):
                grid[(1, col)] = 0
            for col in range(4, width - 1, 4):
                grid[(height - 2, col)] = 0
        else:
            for row in range(1, height - 1, 2):
                for col in range(1, width - 1):
                    grid[(row, col)] = 0
            # add minor passages
            for row in range(2, height - 1, 4):
                grid[(row, 1)] = 0
            for row in range(4, height - 1, 4):
                grid[(row, width - 2)] = 0

        return grid

    def _generate_spiral_maze(self, grid):
        """ Create a simple maze that has a spiral path from
        start to end. This is a unicursal maze (with no dead ends).
        """
        clockwise = randint(0, 1)
        # define the directions you will turn
        if clockwise == 1:
            directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        else:
            directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]

        current = (1, 1)
        grid[current] = 0
        next_dir = 0
        while True:
            next_cell = self._move(current, directions[next_dir])
            ns = self._find_neighbors(current[0], current[1], grid, True)
            if next_cell in ns:
                grid[self._midpoint(current, next_cell)] = 0
                grid[next_cell] = 0
                current = next_cell
            elif len(ns) == 0:
                break
            else:
                next_dir = (next_dir + 1) %4

        return grid

    def _midpoint(self, a, b):
        """ Find the wall cell between to passage cells """
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2

    def _move(self, start, direction):
        """ Convolve a position tuple with a direction tuple to
        generate a new position.
        """
        return (start[0] + direction[0], start[1] + direction[1])
