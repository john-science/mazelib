
from __future__ import absolute_import
from mazelib.generate.MazeGenAlgo import MazeGenAlgo
from mazelib.generate.MazeGenAlgo import np
from random import choice, randrange


class CellularAutomaton(MazeGenAlgo):
    """Cells survive if they have one to four neighbours.
    If a cell has exactly three neighbours, it is born.

    It is similar to Conway's Game of Life in that patterns
    that do not have a living cell adjacent to 1, 4, or 5 other
    living cells in any generation will behave identically to it.
    """

    def __init__(self, w, h, complexity=1.0, density=1.0):
        super(CellularAutomaton, self).__init__(w, h)
        self.complexity = complexity
        self.density = density

    def generate(self):
        # create empty grid
        a = np.empty((self.H, self.W), dtype=np.int8)
        a.fill(0)
        # fill borders
        a[0, :] = a[-1, :] = 1
        a[:, 0] = a[:, -1] = 1
        grid = a

        # adjust complexity and density relative to maze size
        if self.complexity <= 1.0:
            self.complexity = self.complexity * (5.0 * (self.H + self.W))
        if self.density <= 1.0:
            self.density = self.density * (self.h * self.w)

        # create walls
        for i in range(int(self.density)):
            y, x = randrange(0, self.H, 2), randrange(0, self.W, 2)
            grid[y][x] = 1
            for j in range(int(self.complexity)):
                neighbors = self._find_neighbors(y, x, grid, True)  # is wall
                neighbors += self._find_neighbors(y, x, grid)       # is open
                if len(neighbors):
                    r,c = choice(neighbors)
                    if grid[r][c] == 0:
                        grid[r][c] = 1
                        grid[r + (y - r) // 2][c + (x - c) // 2] = 1
                        x, y = c, r

        # ensure all corners are filled
        for r in range(2, self.H - 2, 2):
            for c in range(2, self.W - 2, 2):
                grid[r][c] = 1

        return grid
