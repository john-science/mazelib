
from random import choice,randrange,shuffle
from MazeGenAlgo import MazeArray,MazeGenAlgo


class HuntAndKill(MazeGenAlgo):
    """
    1. Randomly choose a starting cell.
    2. Perform a random walk from the current cel, carving passages to unvisited neighbors,
        until the current cell has no unvisited neighbors.
    3. Select a new grid cell; if it has been visited, walk from it.
    4. Repeat steps 2 and 3 a sufficient number of times that there the probability of a cell
        not being visited is extremely small.

    In this implementation of Hunt-and-kill there are two different ways to select a new grid
        cell in step 2.  The first is serpentine through the grid (the classic solution), the
        second is to randomly select a new cell enough times that the probability of an
        unexplored cell is very, very low. The second option includes a small amount of risk,
        but it creates a more interesting, harder maze.
    """

    def __init__(self, w, h, hunt_order='serpentine'):
        super(HuntAndKill, self).__init__(w, h)

        # the user can define what order to hunt for the next cell in
        if hunt_order == 'random':
            self._hunt_order = self._hunt_random
        else:
            self._hunt_order = self._hunt_serpentine

    def generate(self):
        grid = MazeArray(self.H, self.W)
        
        # find an arbitrary starting position
        current = (randrange(1, self.H, 2), randrange(1, self.W, 2))
        grid[current] = 0

        # perform many random walks, to fill the maze
        num_trials = 0
        while current != (-1, -1):
            self._walk(grid, current)
            current = self._hunt(grid, num_trials)
            num_trials += 1

        return grid

    def _walk(self, grid, start):
        """
        This is a standard random walk. It must start from a visited cell.
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

    def _hunt(self, grid, count):
        """ Based on how this algorithm was configured, choose hunt for the next starting point. """
        return self._hunt_order(grid, count)

    def _hunt_random(self, grid, count):
        """ Select the next cell to walk from, randomly. """
        if count >= (self.H * self.W):
            return (-1, -1)

        return (randrange(1, self.H, 2), randrange(1, self.W, 2))

    def _hunt_serpentine(self, grid, count):
        """ Select the next cell to walk from by cycling through every grid cell in order. """
        cell = (1, 1)
        found = False

        while not found:
            cell = (cell[0], cell[1] + 2)
            if cell[1] > (self.W - 2):
                cell = (cell[0] + 2, 1)
                if cell[0] > (self.H - 2):
                    return (-1, -1)

            if grid[cell] == 0 and len(self._find_neighbors(cell, grid, True)) > 0:
                found = True

        return cell

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
