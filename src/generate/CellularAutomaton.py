from random import choice,randrange
from MazeGenAlgo import MazeArray,MazeGenAlgo


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
        # Adjust complexity and density relative to maze size
        if self.complexity <= 1.0:
            self.complexity = int(self.complexity * (5 * (self.H + self.W)))
        if self.density <= 1.0:
            self.density = int(self.density * (self.h * self.w))

        # Build actual maze
        grid = MazeArray(self.H, self.W, 0)
        # Fill borders
        grid[0, :] = grid[-1, :] = 1
        grid[:, 0] = grid[:, -1] = 1

        # create walls
        for i in xrange(self.density):
            y, x = randrange(0, self.H, 2), randrange(0, self.W, 2)
            grid[y, x] = 1
            for j in xrange(self.complexity):
                neighbours = self.find_neighbors((y, x), grid, True)  # is wall
                neighbours += self.find_neighbors((y, x), grid)       # is open
                if len(neighbours):
                    r,c = choice(neighbours)
                    if grid[r, c] == 0:
                        grid[r, c] = 1
                        grid[r + (y - r) // 2, c + (x - c) // 2] = 1
                        x, y = c, r

        return grid
