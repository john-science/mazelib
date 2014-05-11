
import math
from random import choice,randrange,shuffle
from MazeGenAlgo import MazeArray,MazeGenAlgo


class HuntAndKill(MazeGenAlgo):

    def __init__(self, w, h):
        super(HuntAndKill, self).__init__(w, h)

    def generate(self):
        """
        1. Randomly choose a starting cell.
        2. Perform a random walk from the current cel, carving passages to unvisited neighbors,
            until the current cell has no unvisited neighbors.
        3. Randomly select a new grid cell, if it has been visited, walk from it.
        4. Repeat steps 2 and 3 a sufficient number of times that there the probability of a cell
            not being visited is extremely small.
        """

        grid = MazeArray(self.H, self.W)
        
        # do a random walk from an arbitrary starting position
        start = self._hunt(grid)
        grid[start] = 0
        self._walk(grid, start)
        
        # try to random walk from several random positions
        random_trials = self.H * self.W
        for i in xrange(random_trials):
            current = self._hunt(grid)
            self._walk(grid, current)

        return grid

    def _walk(self, grid, start):
        """
        This is a standard random walk.
        It must start from a visited cell.
        And it completes when the current cell has no unvisited neighbors.
        """
        if grid[start] == 0:
            current = start
            unvisited_neighbors = self._find_neighbors(current, grid, True)

            while len(unvisited_neighbors) >  0:
                neighbor = choice(unvisited_neighbors)
                grid[neighbor] = 0
                grid[(neighbor[0] + current[0]) // 2, (neighbor[1] + current[1]) // 2] = 0
                current = neighbor
                unvisited_neighbors = self._find_neighbors(current, grid, True)
    
    def _hunt(self, grid):
        """ Randomly select the next cell to walk from. """
        return (randrange(1, self.H, 2), randrange(1, self.W, 2))

    # TODO: Several algorithms use this method, should they share it?
    def _find_neighbors(self, posi, grid, unvisited=False):
        """ Find all the neighbors in the grid of the current position,
        that have/haven't been visited.
        """
        (row, col) = posi
        ns = []

        if row > 1 and grid[row-2, col] == unvisited:
            ns.append((row-2, col))
        if row < self.H-2 and grid[row+2, col] == unvisited:
            ns.append((row+2, col))
        if col > 1 and grid[row, col-2] == unvisited:
            ns.append((row, col-2))
        if col < self.W-2 and grid[row, col+2] == unvisited:
            ns.append((row, col+2))

        shuffle(ns)

        return ns
