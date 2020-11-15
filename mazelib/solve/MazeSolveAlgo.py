import abc
import numpy as np
from numpy.random import shuffle


class MazeSolveAlgo:
    __metaclass__ = abc.ABCMeta

    def solve(self, grid, start, end):
        """ helper method to solve a init the solver before solving the maze

        Args:
            grid (np.array): maze array
            start (tuple): position in maze to start from
            end (tuple): position in maze to finish at
        Returns:
            list: final solutions
        """
        self._solve_preprocessor(grid, start, end)
        return self._solve()

    def _solve_preprocessor(self, grid, start, end):
        """ ensure the maze mazes any sense before you solve it

        Args:
            grid (np.array): maze array
            start (tuple): position in maze to start from
            end (tuple): position in maze to finish at
        Returns: None
        """
        self.grid = grid.copy()
        self.start = start
        self.end = end

        # validating checks
        assert grid is not None, 'Maze grid is not set.'
        assert start is not None and end is not None, 'Entrances are not set.'
        assert start[0] >= 0 and start[0] < grid.shape[0], 'Entrance is outside the grid.'
        assert start[1] >= 0 and start[1] < grid.shape[1], 'Entrance is outside the grid.'
        assert end[0] >= 0 and end[0] < grid.shape[0], 'Entrance is outside the grid.'
        assert end[1] >= 0 and end[1] < grid.shape[1], 'Entrance is outside the grid.'

    @abc.abstractmethod
    def _solve(self):
        return None

    """
    All of the methods below this are helper methods,
    common to many maze-solving algorithms.
    """

    def _find_unblocked_neighbors(self, posi):
        """ Find all the grid neighbors of the current position; visited, or not.

        Args:
            posi (tuple): cell of interest
        Returns:
            list: all the unblocked neighbors to this cell
        """
        r, c = posi
        ns = []

        if r > 1 and not self.grid[r - 1, c] and not self.grid[r - 2, c]:
            ns.append((r - 2, c))
        if r < self.grid.shape[0] - 2 and not self.grid[r + 1, c] and not self.grid[r + 2, c]:
            ns.append((r + 2, c))
        if c > 1 and not self.grid[r, c - 1] and not self.grid[r, c - 2]:
            ns.append((r, c - 2))
        if c < self.grid.shape[1] - 2 and not self.grid[r, c + 1] and not self.grid[r, c + 2]:
            ns.append((r, c + 2))

        shuffle(ns)
        return ns

    def _midpoint(self, a, b):
        """ Find the wall cell between to passage cells

        Args:
            a (tuple): first cell
            b (tuple): second cell
        Returns:
            tuple: cell half way between the first two
        """
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2

    def _move(self, start, direction):
        """ Convolve a position tuple with a direction tuple to generate a new position.

        Args:
            start (tuple): position cell to start at
            direction (tuple): vector cell of direction to travel to
        Returns:
            tuple: end result of movement
        """
        return tuple(map(sum, zip(start, direction)))

    def _on_edge(self, cell):
        """ Does the cell lay on the edge, rather inside of the maze grid?

        Args:
            cell (tuple): some place in the grid
        Returns:
            bool: Is the cell on the edge of the maze?
        """
        r, c = cell

        if r == 0 or r == self.grid.shape[0] - 1:
            return True
        if c == 0 or c == self.grid.shape[1] - 1:
            return True

        return False

    def _push_edge(self, cell):
        """ You may need to find the cell directly inside of a start or end cell.

        Args:
            cell (tuple): some place in the grid
        Returns:
            tuple: the new cell location, pushed from the edge
        """
        r, c = cell

        if r == 0:
            return (1, c)
        elif r == (self.grid.shape[0] - 1):
            return (r - 1, c)
        elif c == 0:
            return (r, 1)
        else:
            return (r, c - 1)

    def _within_one(self, cell, desire):
        """ Is the current cell within one move of the desired cell?
        Note, this might be one full more, or one half move.

        Args:
            cell (tuple): position to start at
            desire (tuple): position you want to be at
        Returns:
            bool: Are you within one movement of your goal?
        """
        if not cell or not desire:
            return False

        if cell[0] == desire[0]:
            if abs(cell[1] - desire[1]) < 2:
                return True
        elif cell[1] == desire[1]:
            if abs(cell[0] - desire[0]) < 2:
                return True

        return False

    def _prune_solution(self, solution):
        """ In the process of solving a maze, the algorithm might go down
        the wrong corridor then backtrack. These extraneous steps need to be removed.
        Also, clean up the end points.

        Args:
            solution (list): raw maze solution
        Returns:
            list: cleaner, tightened up solution to the maze
        """
        found = True
        attempt = 0
        max_attempt = len(solution)

        while found and len(solution) > 2 and attempt < max_attempt:
            found = False
            attempt += 1

            for i in range(len(solution) - 1):
                first = solution[i]
                if first in solution[i + 1:]:
                    first_i = i
                    last_i = solution[i + 1:].index(first) + i + 1
                    found = True
                    break

            if found:
                solution = solution[:first_i] + solution[last_i:]

        # solution does not include entrances
        if len(solution) > 1:
            if solution[0] == self.start:
                solution = solution[1:]
            if solution[-1] == self.end:
                solution = solution[:-1]

        return solution

    def prune_solutions(self, solutions):
        """ prune all the duplicate cells from all solutions, and fix end points

        Args:
            solutions (list): multiple raw solutions
        Returns:
            list: the above solutions, cleaned up
        """
        return [self._prune_solution(s) for s in solutions]