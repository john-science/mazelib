
from random import choice, randrange, shuffle
import numpy as np
# If the code is not Cython-compiled, we need to add some imports.
try:
    from cython import compiled
except ModuleNotFoundError:
    compiled = False
if not compiled:
    from mazelib.generate.MazeGenAlgo import MazeGenAlgo

RANDOM = 1
SERPENTINE = 2


class DungeonRooms(MazeGenAlgo):
    """
    This is a variation on Hunt-and-Kill where the initial maze has rooms carved out of
    it, instead of being completely flat.

    Optional Parameters

    rooms: List(List(tuple, tuple))
        A list of lists, containing the top-left and bottom-right grid coords of where
        you want rooms to be created. For best results, the corners of each room should
        have odd-numbered coordinates.
    grid: i8[H,W]
        A pre-built maze array filled with one, or many, rooms.
    hunt_order: String ['random', 'serpentine']
        Determines how the next cell to hunt from will be chosen. (default 'random')
    """

    def __init__(self, h0, w0, rooms=None, grid=None, hunt_order='random'):
        # if the user provides a grid, that overrides h & w
        if grid is not None:
            h = (grid.shape[0] - 1) // 2
            w = (grid.shape[1] - 1) // 2
            self.backup_grid = grid.copy()
        else:
            h = h0
            w = w0
            self.backup_grid = np.empty((2 * h + 1, 2 * w + 1), dtype=np.int8)
            self.backup_grid.fill(1)
        self.grid = None
        self.rooms = rooms
        super(DungeonRooms, self).__init__(h, w)

        # the user can define what order to hunt for the next cell in
        if hunt_order.lower().strip() == 'serpentine':
            self._hunt_order = SERPENTINE
        else:
            self._hunt_order = RANDOM

    def generate(self):
        # define grid and rooms
        self.grid = self.backup_grid.copy()
        self._carve_rooms(self.rooms)

        # select start position for algorithm
        current = self._choose_start()
        self.grid[current[0]][current[1]] = 0

        # perform many random walks, to fill the maze
        num_trials = 0
        while current != (-1, -1):
            self._walk(current)
            current = self._hunt(num_trials)
            num_trials += 1

        # fix any unconnected wall sections
        self._reconnect_maze()

        return self.grid

    def _carve_rooms(self, rooms):
        """ Open up user-defined rooms in a maze. """
        if rooms is None:
            return

        for room in rooms:
            try:
                top_left, bottom_right = room
                self._carve_room(top_left, bottom_right)
                self._carve_door(top_left, bottom_right)
            except Exception:
                # If the user tries to create an invalid room, it is simply ignored.
                pass

    def _carve_room(self, top_left, bottom_right):
        """ Open up a single user-defined room in a maze. """
        for row in range(top_left[0], bottom_right[0] + 1):
            for col in range(top_left[1], bottom_right[1] + 1):
                self.grid[row, col] = 0

    def _carve_door(self, top_left, bottom_right):
        """ Open up a single door in a user-defined room,
        IF that room does not already have a whole wall of doors.
        """
        even_squares = [i for i in list(top_left) + list(bottom_right) if i % 2 == 0]
        if len(even_squares) > 0:
            return

        # find possible doors on all sides of room
        possible_doors = []
        odd_rows = [i for i in range(top_left[0] - 1, bottom_right[0] + 2) if i % 2 == 1]
        odd_cols = [i for i in range(top_left[1] - 1, bottom_right[1] + 2) if i % 2 == 1]

        if top_left[0] > 2:
            possible_doors += zip([top_left[0] - 1] * len(odd_rows), odd_rows)
        if top_left[1] > 2:
            possible_doors += zip(odd_cols, [top_left[1] - 1] * len(odd_cols))
        if bottom_right[0] < self.grid.shape[0] - 2:
            possible_doors += zip([bottom_right[0] + 1] * len(odd_rows), odd_rows)
        if bottom_right[1] < self.grid.shape[1] - 2:
            possible_doors += zip(odd_cols, [bottom_right[1] + 1] * len(odd_cols))

        door = choice(possible_doors)
        self.grid[door[0], door[1]] = 0

    def _walk(self, start):
        """ This is a standard random walk. It must start from a visited cell.
        And it completes when the current cell has no unvisited neighbors.
        """
        if self.grid[start[0], start[1]] == 0:
            current = start
            unvisited_neighbors = self._find_neighbors(current[0], current[1], self.grid, True)

            while len(unvisited_neighbors) > 0:
                neighbor = choice(unvisited_neighbors)
                self.grid[neighbor[0], neighbor[1]] = 0
                self.grid[(neighbor[0] + current[0]) // 2, (neighbor[1] + current[1]) // 2] = 0
                current = neighbor
                unvisited_neighbors = self._find_neighbors(current[0], current[1], self.grid, True)

    def _hunt(self, count):
        """ Based on how this algorithm was configured, choose hunt for the next starting point. """
        if self._hunt_order == SERPENTINE:
            return self._hunt_serpentine(count)
        else:
            return self._hunt_random(count)

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

            if self.grid[cell[0]][cell[1]] == 0 and len(self._find_neighbors(cell[0], cell[1], self.grid, True)) > 0:
                found = True

        return cell

    def _choose_start(self):
        """ Choose a random starting location, that is not already inside a room.
        If no such room exists, the input grid was invalid.
        """
        current = (randrange(1, self.H, 2), randrange(1, self.W, 2))

        LIMIT = self.H * self.W * 2
        num_tries = 1

        # keep looping until you find an unvisited cell
        while num_tries < LIMIT:
            current = (randrange(1, self.H, 2), randrange(1, self.W, 2))
            if self.grid[current[0]][current[1]] == 1:
                return current
            num_tries += 1

        if num_tries >= LIMIT:
            raise TypeError('The grid input to DungeonRooms was invalid.')

        return current

    def _reconnect_maze(self):
        """ If a maze is not fully connected, open up walls until it is. """
        self._fix_disjoint_passages(self._find_all_passages())

    def _find_all_passages(self):
        """ Place all connected passage cells into a set.
        Disjoint passages will be in different sets.
        """
        passages = []

        # go through all cells in the maze
        for r in range(1, self.grid.shape[0], 2):
            for c in range(1, self.grid.shape[1], 2):
                ns = self._find_unblocked_neighbors((r, c))
                current = set(ns + [(r, c)])

                # determine which passage(s) the current neighbors belong in
                found = False
                for i, passage in enumerate(passages):
                    intersect = current.intersection(passage)
                    if len(intersect) > 0:
                        passages[i] = passages[i].union(current)
                        found = True
                        break

                # the current neighbors might be a disjoint set
                if not found:
                    passages.append(current)

        return self._join_intersecting_sets(passages)

    def _fix_disjoint_passages(self, disjoint_passages):
        """ All passages in a maze should be connected """
        while len(disjoint_passages) > 1:
            found = False
            while not found:
                # randomly select a cell in the first passage
                cell = choice(list(disjoint_passages[0]))
                neighbors = self._find_neighbors(cell[0], cell[1], self.grid)
                # determine if that cell has a neighbor in any other passage
                for passage in disjoint_passages[1:]:
                    intersect = [c for c in neighbors if c in passage]
                    # if so, remove the dividing wall, and combine the two passages
                    if len(intersect) > 0:
                        mid = self._midpoint(intersect[0], cell)
                        self.grid[mid[0], mid[1]] = 0
                        disjoint_passages[0] = disjoint_passages[0].union(passage)
                        disjoint_passages.remove(passage)
                        found = True
                        break

    def _find_unblocked_neighbors(self, posi):
        """ Find all the grid neighbors of the current position;
            visited, or not.
        """
        r, c = posi
        ns = []

        if r > 1 and self.grid[r-1][c] == False and self.grid[r-2][c] == False:
            ns.append((r-2, c))
        if r < self.grid.shape[0]-2 and self.grid[r+1][c] == False and self.grid[r+2][c] == False:
            ns.append((r+2, c))
        if c > 1 and self.grid[r][c-1] == False and self.grid[r][c-2] == False:
            ns.append((r, c-2))
        if c < self.grid.shape[1]-2 and self.grid[r][c+1] == False and self.grid[r][c+2] == False:
            ns.append((r, c+2))

        shuffle(ns)

        return ns

    def _join_intersecting_sets(self, list_of_sets):  # TODO: method could be a function
        """ combine sets that have non-zero intersections """
        for i in range(len(list_of_sets) - 1):
            if list_of_sets[i] is None:
                continue

            for j in range(i + 1, len(list_of_sets)):
                if list_of_sets[j] is None:
                    continue
                intersect = list_of_sets[i].intersection(list_of_sets[j])
                if len(intersect) > 0:
                    list_of_sets[i] = list_of_sets[i].union(list_of_sets[j])
                    list_of_sets[j] = None

        return list(filter(lambda l: l is not None, list_of_sets))

    def _midpoint(self, a, b):  # TODO: method could be a function or static
        """ Find the wall cell between to passage cells """
        return ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)
