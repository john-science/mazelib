from random import choice, randrange
# If the code is not Cython-compiled, we need to add some imports.
from cython import compiled
if not compiled:
    from mazelib.transmute.MazeTransmuteAlgo import MazeTransmuteAlgo


class Perturbation(MazeTransmuteAlgo):
    """ The Algorithm

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

    def __init__(self, repeat=1, new_walls=1):
        self.repeat = repeat
        self.new_walls = new_walls
        super(Perturbation, self).__init__()

    def _transmute(self):
        """ master method to slightly pertub the maze a set number of times

        Returns: None
        """
        for i in range(self.repeat):
            # Add a small number of random walls, blocking current passages
            for j in range(self.new_walls):
                self._add_a_random_wall()

            # re-fix the maze
            self._reconnect_maze()

    def _add_a_random_wall(self):
        """ Add a single wall randomly within the maze

        Returns: None
        """
        limit = 2 * self.grid.shape[0] * self.grid.shape[1]
        tries = 0

        found = False
        while not found:
            row = randrange(1, self.grid.shape[0] - 1)
            if row % 2 == 0:
                col = randrange(1, self.grid.shape[1] - 1, 2)
            else:
                col = randrange(2, self.grid.shape[1] - 1, 2)

            if self.grid[row][col] == 0:
                found = True
                self.grid[row][col] = 1
            else:
                tries += 1

            # Emergency Catch: in case all walls in the maze are filled
            if tries > limit:
                return

    def _reconnect_maze(self):
        """ If a maze is not fully connected, open up walls until it is.

        Returns: None
        """
        passages = self._find_all_passages()
        self._fix_disjoint_passages(passages)

    def _find_all_passages(self):
        """ Place all connected passage cells into a set. Disjoint passages will be in different sets.

        Returns:
            list: all of the non-connected paths in the maze
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
        """ All passages in a maze should be connected

        Args:
            disjoint_passages (list): presumably non-connected paths in the maze
        Returns: None
        """
        while len(disjoint_passages) > 1:
            found = False
            while not found:
                # randomly select a cell in the first passage
                cell = choice(list(disjoint_passages[0]))
                neighbors = self._find_neighbors(cell[0], cell[1])
                # determine if that cell has a neighbor in any other passage
                for passage in disjoint_passages[1:]:
                    intersect = [c for c in neighbors if c in passage]
                    # if so, remove the dividing wall, combine the two passages
                    if len(intersect) > 0:
                        mid = self._midpoint(intersect[0], cell)
                        self.grid[mid[0]][mid[1]] = 0
                        disjoint_passages[0] = disjoint_passages[0].union(passage)
                        disjoint_passages.remove(passage)
                        found = True
                        break

    def _join_intersecting_sets(self, list_of_sets):
        """ combine sets that have non-zero intersections

        Args:
            list_of_sets (list): presumably non-connected paths in the maze
        Returns:
            list: definitely non-connected paths in the maze
        """
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