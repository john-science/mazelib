import abc
from random import shuffle


class MazeSolveAlgo(object):
    __metaclass__ = abc.ABCMeta

    def solve(self, grid, start, end):
        self._solve_preprocessor(grid, start, end)
        return self._solve()

    def _solve_preprocessor(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        
        # validating checks
        if grid is None:
            raise UnboundLocalError('Maze grid is not set.')
        elif start is None or end is None:
            raise UnboundLocalError('Entrances are not set.')
        elif start[0] < 0 or start[0] >= grid.height:
            raise ValueError('Entrance is outside the grid.')
        elif start[1] < 0 or start[1] >= grid.width:
            raise ValueError('Entrance is outside the grid.')
        elif end[0] < 0 or end[0] >= grid.height:
            raise ValueError('Entrance is outside the grid.')
        elif end[1] < 0 or end[1] >= grid.width:
            raise ValueError('Entrance is outside the grid.')

    @abc.abstractmethod
    def _solve(self):
        return

    def _find_neighbors(self, posi, is_wall=False):
        """Find all the grid neighbors of the current position;
        wall or open passage.
        """
        (row, col) = posi
        ns = []

        if row > 1 and self.grid[row-2, col] == is_wall:
            ns.append((row-2, col))
        if row < self.grid.height-2 and self.grid[row+2, col] == is_wall:
            ns.append((row+2, col))
        if col > 1 and self.grid[row, col-2] == is_wall:
            ns.append((row, col-2))
        if col < self.grid.width-2 and self.grid[row, col+2] == is_wall:
            ns.append((row, col+2))

        shuffle(ns)

        return ns
