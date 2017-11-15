
from __future__ import absolute_import
from mazelib.generate.MazeGenAlgo import MazeGenAlgo
from mazelib.generate.MazeGenAlgo import np
from random import randint


class TrivialMaze(MazeGenAlgo):
    """
    The Algorithm

    This is actually a collection of little tools to make simple,
    unicursal mazes. Currently, there are two trivial mazes available:
    serpentine and spiral.
    """

    def __init__(self, h, w, maze_type='spiral'):
        if maze_type == 'serpentine':
            self.sub_gen = self._generate_serpentine_maze
        elif maze_type == 'spiral':
            self.sub_gen = self._generate_spiral_maze
        else:
            self.sub_gen = self._generate_spiral_maze

        super(TrivialMaze, self).__init__(h, w)

    def generate(self):
        # create empty grid
        a = np.empty((self.H, self.W), dtype=np.int8)
        a.fill(1)
        grid = a

        grid = self.sub_gen(grid)

        return grid

    def _generate_serpentine_maze(self, grid):
        """Create a simple maze that snakes around the grid.
        This is a unicursal maze (with no dead ends).
        """
        vertical_bias = randint(0, 1)

        if vertical_bias:
            for row in range(1, grid.height - 1):
                for col in range(1, grid.width - 1, 2):
                    grid[(row, col)] = 0
            # add minor passages
            for col in range(2, grid.width - 1, 4):
                grid[(1, col)] = 0
            for col in range(4, grid.width - 1, 4):
                grid[(grid.height - 2, col)] = 0
        else:
            for row in range(1, grid.height - 1, 2):
                for col in range(1, grid.width - 1):
                    grid[(row, col)] = 0
            # add minor passages
            for row in range(2, grid.height - 1, 4):
                grid[(row, 1)] = 0
            for row in range(4, grid.height - 1, 4):
                grid[(row, grid.width - 2)] = 0

        return grid

    def _generate_spiral_maze(self, grid):
        """Create a simple maze that has a spiral path from
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
        """Find the wall cell between to passage cells"""
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2

    def _move(self, start, direction):
        """Convolve a position tuple with a direction tuple to
        generate a new position.
        """
        return (start[0] + direction[0], start[1] + direction[1])
