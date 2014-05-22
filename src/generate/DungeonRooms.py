
from random import randrange,shuffle
from MazeGenAlgo import MazeGenAlgo


class DungeonRooms(MazeGenAlgo):

    def __init__(self, grid):
        h = (grid.height - 1) // 2
        w = (grid.width - 1) // 2
        self.grid = grid
        super(DungeonRooms, self).__init__(h, w)

    def generate(self):
        current = self._choose_start()
        self.grid[current] = 0

        # created a weighted list of all vertices connected in the graph
        neighbors = self.find_neighbors(current, self.grid, False)

        # loop over all current neighbors, until empty
        visited = self._number_visited()
        while visited < self.h * self.w:
            # find neighbor with lowest weight, make it current
            nn = randrange(len(neighbors))
            current = neighbors[nn]
            visited += 1
            self.grid[current] = 0
            neighbors = neighbors[:nn] + neighbors[nn + 1:]

            # connect that neighbor to a random previously-visited neighbor
            nearest_n = self.find_neighbors(current, self.grid)[0]
            self.grid[(current[0] + nearest_n[0]) // 2, (current[1] + nearest_n[1]) // 2] = 0

            # find all unvisited neighbors of current, add them to neighbors
            unvisited = self.find_neighbors(current, self.grid, False)
            for unv in unvisited:
                if unv not in neighbors:
                    neighbors.append(unv)

        return self.grid

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
    
    def _number_visited(self):
        """Determine the number of grid cells already visited,
        including those in the input grid rooms.
        """
        visited = 0

        for r in xrange(1, self.H, 2):
            for c in xrange(1, self.W, 2):
                if self.grid[r,c] == 0:
                    visited += 1

        if visited >= self.h * self.h:
            raise ValueError('The grid input to DungeonRooms was invalid.')

        return visited
