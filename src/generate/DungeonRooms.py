
from random import choice,randrange,shuffle
from MazeGenAlgo import MazeArray,MazeGenAlgo


class DungeonRooms(MazeGenAlgo):
    """

    0. Start with a grid which already includes open rooms.
    1. Randomly choose a starting cell.
    2. Perform a random walk from the current cel, carving passages to unvisited neighbors,
    until the current cell has no unvisited neighbors.
    3. Select a new grid cell; if it has been visited, walk from it.
    4. Repeat steps 2 and 3 a sufficient number of times that there the probability of a cell
    not being visited is extremely small.

    This implementation of DungeonRooms is based on the classic Hunt-and-Kill algorithm.
    
    There are two different ways to select a new grid cell in step 2.
    The first is serpentine through the grid (the classic solution), the second is to
    randomly select a new cell enough times that the probability of anunexplored cell is
    very, very low. The second option includes a small amount of risk, but it creates a
    more interesting, harder maze.
    """

    def __init__(self, grid, hunt_order='random'):
        h = (grid.height - 1) // 2
        w = (grid.width - 1) // 2
        self.grid = grid
        super(DungeonRooms, self).__init__(w, h)

        # the user can define what order to hunt for the next cell in
        if hunt_order == 'random':
            self._hunt_order = self._hunt_random
        elif hunt_order == 'serpentine':
            self._hunt_order = self._hunt_serpentine
        else:
            self._hunt_order = self._hunt_random

    def generate(self):
        current = self._choose_start()
        self.grid[current] = 0
        
        # find an arbitrary starting position
        current = (randrange(1, self.H, 2), randrange(1, self.W, 2))
        self.grid[current] = 0

        # perform many random walks, to fill the maze
        num_trials = 0
        while current != (-1, -1):
            self._walk(self.grid, current)
            current = self._hunt(self.grid, num_trials)
            num_trials += 1

        return self.grid

    def _walk(self, start):
        """
        This is a standard random walk. It must start from a visited cell.
        And it completes when the current cell has no unvisited neighbors.
        """
        if self.grid[start] == 0:
            current = start
            unvisited_neighbors = self.find_neighbors(current, self.grid, False)

            while len(unvisited_neighbors) > 0:
                neighbor = choice(unvisited_neighbors)
                self.grid[neighbor] = 0
                self.grid[(neighbor[0] + current[0]) // 2, (neighbor[1] + current[1]) // 2] = 0
                current = neighbor
                unvisited_neighbors = self.find_neighbors(current, self.grid, False)

    def _hunt(self, count):
        """ Based on how this algorithm was configured, choose hunt for the next starting point. """
        return self._hunt_order(self.grid, count)

    def _hunt_random(self, count):
        """ Select the next cell to walk from, randomly. """
        if count >= (self.H * self.W):
            return (-1, -1)

        return (randrange(1, self.H, 2), randrange(1, self.W, 2))

    def _hunt_serpentine(self, count):
        """ Select the next cell to walk from by cycling through every grid cell in order. """
        cell = (1, 1)
        found = False

        while not found:
            cell = (cell[0], cell[1] + 2)
            if cell[1] > (self.W - 2):
                cell = (cell[0] + 2, 1)
                if cell[0] > (self.H - 2):
                    return (-1, -1)

            if self.grid[cell] == 0 and len(self.find_neighbors(cell, self.grid, False)) > 0:
                found = True

        return cell
        
    def _choose_start(self):
        """Choose a random starting location, that is not already inside a room.
        If no such room exists, the input grid was invalid.
        """
        current = (randrange(1, self.H, 2), randrange(1, self.W, 2))

        LIMIT = self.H * self.W * 2
        num_tries = 1

        # keep looping until you find an unvisited cell
        while self.grid[current] == 1 and num_tries < LIMIT:
            current = (randrange(1, self.H, 2), randrange(1, self.W, 2))
            num_tries += 1

        if num_tries >= LIMIT:
            raise UnboundError('The grid input to DungeonRooms was invalid.')

        return current
