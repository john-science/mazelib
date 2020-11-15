# If the code is not Cython-compiled, we need to add some imports.
from cython import compiled
if not compiled:
    from mazelib.transmute.MazeTransmuteAlgo import MazeTransmuteAlgo


class DeadEndFiller(MazeTransmuteAlgo):
    """ The Algorithm

    1. Scan the maze in any order, looking for dead ends.
    2. Fill in each dead end, and any dead-end passages attached to them.

    Optionally, run the above multiple times to find more dead ends.
    Eventually, if you start with a perfect maze, you will end up with only solution cells left
    open in your maze.
    """

    def __init__(self, iterations=1):
        self.iterations = int(iterations) if iterations > 0 else 100
        super(DeadEndFiller, self).__init__()

    def _transmute(self):
        """ master method to fill in all the dead ends in the maze

        Returns: None
        """
        # make sure we don't block off the entrances
        r, c = self.start
        start_save = self.grid[r, c]
        self.grid[r, c] = 0
        r, c = self.end
        end_save = self.grid[r, c]
        self.grid[r, c] = 0

        # block off all the dead ends N times
        found = True
        i = 0
        while found and i < self.iterations:
            i += 1
            found = self._fill_dead_ends()

        # re-set start and end
        r, c = self.start
        self.grid[r, c] = start_save
        r, c = self.end
        self.grid[r, c] = end_save

    def _fill_dead_ends(self):
        """ fill all dead ends in the maze

        Returns:
            bool: Where any dead ends found in the maze?
        """
        # loop through the maze serpentine, and find dead ends
        dead_end = self._find_dead_end()
        found = False
        while dead_end != (-1, -1):
            found = True

            # fill-in and wall-off the dead end
            self._fill_dead_end(dead_end)

            # from the dead end, travel one cell
            ns = self._find_unblocked_neighbors(dead_end)

            if len(ns) == 0:
                break

            # look at the next cell, if it is a dead end, restart the loop
            if len(ns) == 1:
                # continue until you are in a junction cell
                if self._is_dead_end(ns[0]):
                    dead_end = ns[0]
                    continue

            # otherwise, find another dead end in the maze
            dead_end = self._find_dead_end()

        return found

    def _fill_dead_end(self, dead_end):
        """ After moving from a dead end, we want to fill in it and all the walls around it.

        Args:
            dead_end (tuple): position of the dead end we want to fill in
        Returns: None
        """
        r, c = dead_end
        self.grid[r, c] = 1
        self.grid[r - 1, c] = 1
        self.grid[r + 1, c] = 1
        self.grid[r, c - 1] = 1
        self.grid[r, c + 1] = 1

    def _find_dead_end(self):
        """ A "dead end" is a cell with only zero or one open neighbors. The start end end count as open.

        Returns:
            tuple: position of another dead end in the maze. (returns (-1, -1) if one can't be found)
        """
        for r in range(1, self.grid.shape[0], 2):
            for c in range(1, self.grid.shape[1], 2):
                if self._within_one((r, c), self.start):
                    continue
                elif self._within_one((r, c), self.end):
                    continue
                elif self._is_dead_end((r, c)):
                    return (r, c)

        return (-1, -1)

    def _is_dead_end(self, cell):
        """ Is this cell a dead end? A dead end has zero or one open neighbors

        Args:
            cell (tuple): maze position of interest
        Returns:
            bool: Is this cell a dead end?
        """
        ns = self._find_unblocked_neighbors(cell)

        if self.grid[cell[0], cell[1]] == 1:
            return False
        elif len(ns) < 2:
            return True
        else:
            return False