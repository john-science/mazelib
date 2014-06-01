
from random import choice,randrange,shuffle
from MazeGenAlgo import MazeArray,MazeGenAlgo


class DungeonRooms(MazeGenAlgo):
    """
    The Algorithm

    This is a variation on Hunt-and-Kill where the initial maze has rooms carved out of
    it, instead of being completely flat.

    Optional Parameters

    rooms: List(List(tuple, tuple))
        A list of lists, containing the top-left and bottom-right grid coords of where
        you want rooms to be created. For best results, the corners of each room should
        have odd-numbered coordinates.
    grid: MazeArray
        A pre-built maze array filled with one, or many, rooms.
    hunt_order: String ['random', 'serpentine']
        Determines how the next cell to hunt from will be chosen. (default 'random')
    """

    def __init__(self, h0, w0, rooms=None, grid=None, hunt_order='random'):
        # if the user provides a grid, that overrides h & w
        if grid:
            h = (grid.height - 1) // 2
            w = (grid.width - 1) // 2
            self.grid = grid
        else:
            h = h0
            w = w0
            self.grid = MazeArray(2 * h + 1, 2 * w + 1)
        super(DungeonRooms, self).__init__(h, w)

        # the user can define what order to hunt for the next cell in
        if hunt_order == 'random':
            self._hunt_order = self._hunt_random
        elif hunt_order == 'serpentine':
            self._hunt_order = self._hunt_serpentine
        else:
            self._hunt_order = self._hunt_random
        
        # the user can provide rectangular rooms to be cut out of the initial maze
        self._carve_rooms(rooms)

    def generate(self):
        current = self._choose_start()
        self.grid[current] = 0
        
        # find an arbitrary starting position
        current = (randrange(1, self.H, 2), randrange(1, self.W, 2))
        self.grid[current] = 0

        # perform many random walks, to fill the maze
        num_trials = 0
        while current != (-1, -1):
            self._walk(current)
            current = self._hunt(num_trials)
            num_trials += 1

        return self.grid

    def _carve_rooms(self, rooms):
        """Open up user-defined rooms in a maze."""
        if rooms is None:
            return

        for room in rooms:
            try:
                top_left,bottom_right = room
                self._carve_room(top_left, bottom_right)
                self._carve_door(top_left, bottom_right)
            except Exception:
                # If the user tries to create an invalid room, it is simply ignored.
                pass

    def _carve_room(self, top_left, bottom_right):
        """Open up a single user-defined room in a maze."""
        for row in xrange(top_left[0], bottom_right[0] + 1):
                for col in xrange(top_left[1], bottom_right[1] + 1):
                    self.grid[row, col] = 0

    def _carve_door(self, top_left, bottom_right):
        """Open up a single door in a user-defined room,
        IF that room does not already have a whole wall of doors."""
        even_squares = filter(lambda i: i % 2 == 0, list(top_left) + list(bottom_right))
        if len(even_squares) > 0:
            return

        # find possible doors on all sides of room
        possible_doors = []
        odd_rows = filter(lambda i: i % 2 == 1, range(top_left[0] - 1, bottom_right[0] + 2))
        odd_cols = filter(lambda i: i % 2 == 1, range(top_left[1] - 1, bottom_right[1] + 2))

        if top_left[0] > 2:
            possible_doors += zip([top_left[0] - 1] * len(odd_rows), odd_rows)
        if top_left[1] > 2:
            possible_doors += zip(odd_cols, [top_left[1] - 1] * len(odd_cols))
        if bottom_right[0] < self.grid.height - 2:
            possible_doors += zip([bottom_right[0] + 1] * len(odd_rows), odd_rows)
        if bottom_right[1] < self.grid.width - 2:
            possible_doors += zip(odd_cols, [bottom_right[1] + 1] * len(odd_cols))

        door = choice(possible_doors)
        self.grid[door] = 0

    def _walk(self, start):
        """
        This is a standard random walk. It must start from a visited cell.
        And it completes when the current cell has no unvisited neighbors.
        """
        if self.grid[start] == 0:
            current = start
            unvisited_neighbors = self.find_neighbors(current, self.grid, True)

            while len(unvisited_neighbors) > 0:
                neighbor = choice(unvisited_neighbors)
                self.grid[neighbor] = 0
                self.grid[(neighbor[0] + current[0]) // 2, (neighbor[1] + current[1]) // 2] = 0
                current = neighbor
                unvisited_neighbors = self.find_neighbors(current, self.grid, True)

    def _hunt(self, count):
        """ Based on how this algorithm was configured, choose hunt for the next starting point. """
        return self._hunt_order(count)

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

            if self.grid[cell] == 0 and len(self.find_neighbors(cell, self.grid, True)) > 0:
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
