import abc
import copy
from random import shuffle


class MazeSolveAlgo(object):
    __metaclass__ = abc.ABCMeta

    def solve(self, grid, start, end):
        self._solve_preprocessor(grid, start, end)
        return self._solve()

    def _solve_preprocessor(self, grid, start, end):
        self.grid = copy.deepcopy(grid)
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
        r, c = posi
        ns = []

        if r > 1 and self.grid[r-2, c] == is_wall:
            ns.append((r-2, c))
        if r < self.grid.height-2 and self.grid[r+2, c] == is_wall:
            ns.append((r+2, c))
        if c > 1 and self.grid[r, c-2] == is_wall:
            ns.append((r, c-2))
        if c < self.grid.width-2 and self.grid[r, c+2] == is_wall:
            ns.append((r, c+2))

        shuffle(ns)

        return ns

    def _find_unblocked_neighbors(self, posi):
        """Find all the grid neighbors of the current position;
        visited, or not.
        """
        r, c = posi
        ns = []

        if r > 1 and self.grid[r-1, c] == False and self.grid[r-2, c] == False:
            ns.append((r-2, c))
        if r < self.grid.height-2 and self.grid[r+1, c] == False and self.grid[r+2, c] == False:
            ns.append((r+2, c))
        if c > 1 and self.grid[r, c-1] == False and self.grid[r, c-2] == False:
            ns.append((r, c-2))
        if c < self.grid.width-2 and self.grid[r, c+1] == False and self.grid[r, c+2] == False:
            ns.append((r, c+2))

        shuffle(ns)

        return ns

    def _midpoint(self, a, b):
        """Find the wall cell between to passage cells"""
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2

    def _on_edge(self, cell):
        """Does the cell lay on the edge, rather inside of the maze grid?"""
        r, c = cell
        
        if r == 0 or r == self.grid.height - 1:
            return True
        if c == 0 or c == self.grid.width - 1:
            return True

        return False
