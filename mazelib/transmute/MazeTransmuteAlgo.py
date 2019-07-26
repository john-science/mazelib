import abc
from numpy.random import shuffle


class MazeTransmuteAlgo:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.grid = None
        self.start = None
        self.end = None

    def transmute(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        self._transmute()

    @abc.abstractmethod
    def _transmute(self):
        pass

    """
    All of the methods below this are helper methods,
    common to many maze-transmuting algorithms.
    """

    def _find_unblocked_neighbors(self, posi):
        """ Find all the grid neighbors of the current position; visited, or not. """
        r, c = posi
        ns = []

        if r > 1 and self.grid[r-1, c] == False and self.grid[r-2, c] == False:
            ns.append((r-2, c))
        if r < self.grid.shape[0]-2 and self.grid[r+1, c] == False and self.grid[r+2, c] == False:
            ns.append((r+2, c))
        if c > 1 and self.grid[r, c-1] == False and self.grid[r, c-2] == False:
            ns.append((r, c-2))
        if c < self.grid.shape[1]-2 and self.grid[r, c+1] == False and self.grid[r, c+2] == False:
            ns.append((r, c+2))

        shuffle(ns)

        return ns

    def _find_neighbors(self, r, c, is_wall=False):
        """ Find all the grid neighbors of the current position; visited, or not.
        """
        ns = []

        if r > 1 and self.grid[r - 2][c] == is_wall:
            ns.append((r - 2, c))
        if r < self.grid.shape[0] - 2 and self.grid[r + 2][c] == is_wall:
            ns.append((r + 2, c))
        if c > 1 and self.grid[r][c - 2] == is_wall:
            ns.append((r, c - 2))
        if c < self.grid.shape[1] - 2 and self.grid[r][c + 2] == is_wall:
            ns.append((r, c + 2))

        shuffle(ns)

        return ns

    def _within_one(self, cell, desire):
        """ Is the current cell within one move of the desired cell?
        Note, this might be one full more, or one half move.
        """
        if not cell or not desire:
            return False

        if cell[0] == desire[0]:
            if abs(cell[1] - desire[1]) < 2:
                return True
        elif cell[1] == desire[1]:
            if abs(cell[0] - desire[0]) < 2:
                return True

        return False

    def _midpoint(self, a, b):
        """ Find the wall cell between to passage cells """
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2
