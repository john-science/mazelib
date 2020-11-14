# If the code is not Cython-compiled, we need to add some imports.
from cython import compiled
if not compiled:
    from mazelib.transmute.MazeTransmuteAlgo import MazeTransmuteAlgo


class CuldeSacFiller(MazeTransmuteAlgo):
    """ This algorithm could be called LoopFiller, because it breaks up loop in the maze.

    1. Scan the maze, looking for cells with connecting halls that go in exactly two directions.
    2. At each of these places, travel in both directions until you find your first intersection.
    3. If the first intersection for both paths is the same, you have a loop.
    4. Fill in the cell you started at with a wall, breaking the loop.
    """

    def _transmute(self):
        """ Master methot to fill in all the loops in the maze

        Returns: None
        """
        for r in range(1, self.grid.shape[0], 2):
            for c in range(1, self.grid.shape[1], 2):
                if (r, c) in (self.start, self.end):
                    # we don't want to block off an exit
                    continue
                elif self.grid[(r, c)] == 1:
                    # it's a wall, who cares
                    continue

                # determine if we could even possibly be in a loop
                ns = self._find_unblocked_neighbors((r, c))
                if len(ns) != 2:
                    continue

                # travel in both directions until you hit the first intersection
                try:
                    end1 = self._find_next_intersection([(r, c), ns[0]])
                    end2 = self._find_next_intersection([(r, c), ns[1]])
                except AssertionError:
                    continue

                # Found a loop!
                if end1 == end2:
                    self.grid[(r, c)] = 1

    def _find_next_intersection(self, path_start):
        """ Starting with the first two cells in a path, follow the path until you hit the next
        intersection (or dead end)

        Args:
            path_start (list): the first two cells (tuples) in the path you want to travel
        Returns:
            tuple: the location of the first intersection (or dead end) in the maze
        """
        assert len(path_start) == 2, "invalid starting path to travel"

        # save off starting positions for comparisons later
        first = path_start[0]
        previous = path_start[0]
        current = path_start[1]

        # keep traveling until you hit an intersection
        ns = self._find_unblocked_neighbors(current)
        while len(ns) == 2:
            # travel away from where you came from
            if ns[0] == previous:
                previous = current
                current = ns[1]
            else:
                previous = current
                current = ns[0]

            # Edge Case: You looped without finding ANY intersections? Eww.
            if current == first:
                return previous

            # look around for you next traveling position
            ns = self._find_unblocked_neighbors(current)

        return current