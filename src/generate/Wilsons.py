
from random import randrange,shuffle
from MazeGenAlgo import MazeGenAlgo


class Wilsons(MazeGenAlgo):

    def __init__(self, w, h):
        super(Wilsons, self).__init__(w, h, hunt_order='serpentine')

        # the user can define what order to hunt for the next cell in
        if hunt_order == 'random':
            self._hunt_order = self._hunt_random
        else:
            self._hunt_order = self._hunt_serpentine

    def generate(self):
        """
        http://weblog.jamisbuck.org/2011/1/20/maze-generation-wilson-s-algorithm

        Choose any vertex at random and add it to the UST.
        Select any vertex that is not already in the UST and perform a random walk until you
            encounter a vertex that is in the UST.
        Add the vertices and edges touched in the random walk to the UST.
        Repeat 2 and 3 until all vertices have been added to the UST.
        """

        grid = MazeArray(self.H, self.W)
        
        # find an arbitrary starting position
        current = (randrange(1, self.H, 2), randrange(1, self.W, 2))
        grid[current] = 0

        raise NotImplementedError('Algorithm not yet implemented.')

        # perform many random walks, to fill the maze
        num_trials = 0
        while current != (-1, -1):
            self._generate_random_walk(grid, current)
            self._solve_random_walk(grid, current)
            current = self._hunt(grid, num_trials)
            num_trials += 1

        return grid

    def _generate_random_walk(self, grid, start):
        pass

    def _solve_random_walk(self, grid, walk_path):
        pass

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
