
from random import choice, shuffle
# If the code is not Cython-compiled, we need to add some imports.
try:
    from cython import compiled
except ModuleNotFoundError:
    compiled = False
if not compiled:
    from mazelib.solve.MazeSolveAlgo import MazeSolveAlgo
    from mazelib.solve.ShortestPaths import ShortestPaths


class DeadEndFiller(MazeSolveAlgo):
    """
    1. Scan the maze in any order, looking for dead ends.
    2. Fill in each dead end, and any dead-end passages attached to them.
    3. What you will get is a maze with only solution tiles.
    4. Use a different solver (ShortestPaths) to build a solution path.
    """
    def __init__(self, solver=None):
        if not solver:
            self.solver = ShortestPaths()
        else:
            self.solver = solver

    def _solve(self):
        r, c = self.start
        self.grid[r, c] = 0
        r, c = self.end
        self.grid[r, c] = 0
        self._fill_dead_ends()

        return self._build_solutions()

    def _build_solutions(self):
        """ Now that all of the dead ends have been cut out, the maze still needs to be solved. """
        return self.solver.solve(self.grid, self.start, self.end)

    def _fill_dead_ends(self):
        """ fill all dead ends in the maze """
        # loop through the maze serpentine, and find dead ends
        dead_end = self._find_dead_end()
        while dead_end != (-1, -1):
            # fill-in and wall-off the dead end
            self._fill_dead_end(dead_end)

            # from the dead end, travel one cell
            ns = self._find_unblocked_neighbors(dead_end)

            if len(ns) == 0: break

            # look at the next cell, if it is a dead end, restart the loop
            if len(ns) == 1:
                # continue until you are in a junction cell
                if self._is_dead_end(ns[0]):
                    dead_end = ns[0]
                    continue

            # otherwise, find another dead end in the maze
            dead_end = self._find_dead_end()

    def _fill_dead_end(self, dead_end):
        """ After moving from a dead end, we want to fill in it and all the walls around it.
        """
        r,c = dead_end
        self.grid[r, c] = 1
        self.grid[r - 1, c] = 1
        self.grid[r + 1, c] = 1
        self.grid[r, c - 1] = 1
        self.grid[r, c + 1] = 1

    def _find_dead_end(self):
        """ A "dead end" is a cell with only zero or one open neighbors.
        The start end end count as open.
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
        """ A dead end has zero or one open neighbors. """
        ns = self._find_unblocked_neighbors(cell)

        if self.grid[cell[0], cell[1]] == 1:
            return False
        elif len(ns) < 2:
            return True
        else:
            return False
