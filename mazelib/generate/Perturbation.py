from random import choice, randrange, shuffle
import numpy as np
# If the code is not Cython-compiled, we need to add some imports.
try:
    from cython import compiled
except ModuleNotFoundError:
    compiled = False
if not compiled:
    from mazelib.generate.MazeGenAlgo import MazeGenAlgo


class Perturbation(MazeGenAlgo):
    """
    The Algorithm

    1. Start with a complete, valid maze.
    2. Add a small number of random walls, blocking current passages.
    3. Go through the maze and reconnect all passages that are not currently open,
        by randomly opening walls.
    4. Repeat steps 3 and 4 a prescribed number of times.

    Optional Parameters

    new_walls: Integer [1, ...)
        The number of randomly positioned new walls you create throughout the maze. (default 1)
    repeat: Integer [1, ...)
        The number of times sets of new walls will be added to the maze;
        the maze being fixed after each set. (default 1)
    """

    def __init__(self, grid, repeat=1, new_walls=1):
        h = (grid.shape[0] - 1) // 2
        w = (grid.shape[1] - 1) // 2
        self.grid = grid.copy()
        self.repeat = repeat
        self.new_walls = new_walls
        super(Perturbation, self).__init__(h, w)

    def generate(self):
        for i in range(self.repeat):
            # Add a small number of random walls, blocking current passages
            for j in range(self.new_walls):
                self.grid = self._add_a_random_wall(self.grid)

            # re-fix the maze
            self.grid = self._reconnect_maze(self.grid)

        return self.grid

    def _add_a_random_wall(self, grid):
        """ Add a single wall randomly within the maze """
        limit = 2 * grid.shape[0] * grid.shape[1]
        tries = 0

        found = False
        while not found:
            row = randrange(1, grid.shape[0] - 1)
            if row % 2 == 0:
                col = randrange(1, grid.shape[1] - 1, 2)
            else:
                col = randrange(2, grid.shape[1] - 1, 2)

            if grid[row][col] == 0:
                found = True
                grid[row][col] = 1
            else:
                tries += 1

            # Emergency Catch: in case all walls in the maze are filled
            if tries > limit:
                return grid

        return grid

    def _reconnect_maze(self, grid):
        """ If a maze is not fully connected, open up walls until it is. """
        passages = self._find_all_passages(grid)
        return self._fix_disjoint_passages(passages, grid)

    def _find_all_passages(self, grid):
        """ Place all connected passage cells into a set.
            Disjoint passages will be in different sets.
        """
        passages = []

        # go through all cells in the maze
        for r in range(1, grid.shape[0], 2):
            for c in range(1, grid.shape[1], 2):
                ns = self._find_unblocked_neighbors(grid, (r, c))
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

    def _fix_disjoint_passages(self, disjoint_passages, grid):
        """ All passages in a maze should be connected """
        while len(disjoint_passages) > 1:
            found = False
            while not found:
                # randomly select a cell in the first passage
                cell = choice(list(disjoint_passages[0]))
                neighbors = self._find_neighbors(cell[0], cell[1], grid)
                # determine if that cell has a neighbor in any other passage
                for passage in disjoint_passages[1:]:
                    intersect = [c for c in neighbors if c in passage]
                    # if so, remove the dividing wall, combine the two passages
                    if len(intersect) > 0:
                        mid = self._midpoint(intersect[0], cell)
                        grid[mid[0]][mid[1]] = 0
                        disjoint_passages[0] = disjoint_passages[0].union(passage)
                        disjoint_passages.remove(passage)
                        found = True
                        break

        return grid

    def _join_intersecting_sets(self, list_of_sets):
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

    def _find_unblocked_neighbors(self, grid, posi):
        """ Find all the grid neighbors of the current position; visited, or not. """
        r, c = posi
        ns = []

        if r > 1 and grid[r-1][c] == False and grid[r-2][c] == False:
            ns.append((r-2, c))
        if r < grid.shape[0]-2 and grid[r+1][c] == False and grid[r+2][c] == False:
            ns.append((r+2, c))
        if c > 1 and grid[r][c-1] == False and grid[r][c-2] == False:
            ns.append((r, c-2))
        if c < grid.shape[1]-2 and grid[r][c+1] == False and grid[r][c+2] == False:
            ns.append((r, c+2))

        shuffle(ns)

        return ns

    def _midpoint(self, a, b):
        """ Find the wall cell between to passage cells """
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2
