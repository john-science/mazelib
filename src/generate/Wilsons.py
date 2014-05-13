
from random import choice,randrange,shuffle
from MazeGenAlgo import MazeArray,MazeGenAlgo


class Wilsons(MazeGenAlgo):
    """
    Choose any vertex at random and add it to the UST.
    Select any vertex that is not already in the UST and perform a random walk until you
        encounter a vertex that is in the UST.
    Add the vertices and edges touched in the random walk to the UST.
    Repeat 2 and 3 until all vertices have been added to the UST.
    """

    def __init__(self, w, h, hunt_order='serpentine'):
        super(Wilsons, self).__init__(w, h)

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
            walk = self._generate_random_walk(grid, current)
            self._solve_random_walk(grid, walk, current)
            current = self._hunt(grid, num_trials)
            num_trials += 1

        return grid

    def _generate_random_walk(self, grid, start):
        direction = self._random_dir(start)
        walk = {}
        walk[start] = direction
        current = self._move(start, direction)

        while grid[current] == 1:
            direction = self._random_dir(current)
            walk[current] = direction
            current = self._move(current, direction)

        return walk

    def _random_dir(self, current):
        """ Take a step on one random (but valid) direction """
        r,c = current
        options = []
        if r > 1:            options.append(0)  # North
        if r < (self.H - 2): options.append(1)  # South
        if c > 1:            options.append(2)  # East
        if c < (self.W - 2): options.append(3)  # West

        direction = choice(options)
        if direction == 0:   return (-2, 0)  # North
        elif direction == 1: return (2, 0)   # South
        elif direction == 2: return (0, -2)  # East
        else:                return (0, 2)   # West

    def _move(self, start, direction):
        return tuple(map(sum, zip(start, direction)))

    def _solve_random_walk(self, grid, walk, start):
        current = start

        while current in walk:
            next_cell = self._move(current, walk[current])
            grid[next_cell] = 0
            grid[((next_cell[0] + current[0]) // 2, (next_cell[1] + current[1]) // 2)] = 0
            current = next_cell
            if grid[current] == 0:
                break

    def _hunt(self, grid, count):
        """ Based on how this algorithm was configured, choose hunt for the next starting point. """
        return self._hunt_order(grid, count)

    def _hunt_random(self, grid, count):
        """ Select the next cell to walk from, randomly. """
        if count >= (self.H * self.W + 2):
            return (-1, -1)

        return (randrange(1, self.H, 2), randrange(1, self.W, 2))

    def _hunt_serpentine(self, grid, count):
        """ Select the next cell to walk from by cycling through every grid cell in order. """
        cell = (1, -1)
        found = False

        while not found:
            cell = (cell[0], cell[1] + 2)
            if cell[1] > (self.W - 2):
                cell = (cell[0] + 2, 1)
                if cell[0] > (self.H - 2):
                    return (-1, -1)

            if grid[cell] == 0 and len(self._find_neighbors(cell, grid, False)) > 0:
                found = True

        return cell

    # TODO: Several algorithms use this method, should they share it? (Add it to MazeGenAlgo?)
    def _find_neighbors(self, posi, grid, visited=True):  # TODO: Note, I changed this from 'unvisited' to 'visited'.  Fix this in Hunt-and-Kill
        """ Find all the neighbors in the grid of the current position,
        that have/haven't been visited.
        """
        (row, col) = posi
        ns = []

        if row > 1 and grid[row-2, col] == visited:
            ns.append((row-2, col))
        if row < self.H-2 and grid[row+2, col] == visited:
            ns.append((row+2, col))
        if col > 1 and grid[row, col-2] == visited:
            ns.append((row, col-2))
        if col < self.W-2 and grid[row, col+2] == visited:
            ns.append((row, col+2))

        shuffle(ns)

        return ns
