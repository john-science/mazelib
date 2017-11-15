
from random import shuffle


class MazeSolveAlgo(object):

    def solve(self, grid, start, end):
        self._solve_preprocessor(grid, start, end)
        return self._solve()

    def _solve_preprocessor(self, grid, start, end):
        self.grid = grid.copy()
        self.start = start
        self.end = end

        # validating checks
        if grid is None:
            raise UnboundLocalError('Maze grid is not set.')
        elif start is None or end is None:
            raise UnboundLocalError('Entrances are not set.')
        elif start[0] < 0 or start[0] >= grid.shape[0]:
            raise ValueError('Entrance is outside the grid.')
        elif start[1] < 0 or start[1] >= grid.shape[1]:
            raise ValueError('Entrance is outside the grid.')
        elif end[0] < 0 or end[0] >= grid.shape[0]:
            raise ValueError('Entrance is outside the grid.')
        elif end[1] < 0 or end[1] >= grid.shape[1]:
            raise ValueError('Entrance is outside the grid.')

    def _solve(self):
        return None

    """
    All of the methods below this are helper methods,
    common to many maze-solving algorithms.
    """

    def _find_neighbors(self, posi, is_wall=False):
        """Find all the grid neighbors of the current position;
        wall or open passage.
        """
        r, c = posi
        ns = []

        if r > 1 and self.grid[r-2][c] == is_wall:
            ns.append((r-2, c))
        if r < self.grid.shape[0]-2 and self.grid[r+2][c] == is_wall:
            ns.append((r+2, c))
        if c > 1 and self.grid[r][c-2] == is_wall:
            ns.append((r, c-2))
        if c < self.grid.shape[1]-2 and self.grid[r][c+2] == is_wall:
            ns.append((r, c+2))

        shuffle(ns)

        return ns

    def _find_unblocked_neighbors(self, posi):
        """Find all the grid neighbors of the current position;
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

    def _midpoint(self, a, b):
        """Find the wall cell between to passage cells"""
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2

    def _move(self, start, direction):
        """Convolve a position tuple with a direction tuple to
        generate a new position.
        """
        return tuple(map(sum, zip(start, direction)))

    def _on_edge(self, cell):
        """Does the cell lay on the edge, rather inside of the maze grid?"""
        r, c = cell

        if r == 0 or r == self.grid.shape[0] - 1:
            return True
        if c == 0 or c == self.grid.shape[1] - 1:
            return True

        return False

    def _push_edge(self, cell):
        """You may need to find the cell directly inside of a start or end cell."""
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
        """Is the current cell within one move of the desired cell?
        Note, this might be one full more, or one half move.
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
        """In the process of solving a maze, the algorithm might go down
        the wrong corridor then backtrack.

        These extraneous branches need to be removed.
        """
        found = True
        while found and len(solution) > 2:
            found = False

            for i in range(1, len(solution) - 1):
                if solution[i - 1] != solution[i + 1]:
                    continue
                diff = 1

                while i-diff >= 0 and i+diff < len(solution) and solution[i-diff] == solution[i+diff]:
                    diff += 1
                diff -= 1
                index = i
                found = True
                break

            if found:
                for ind in range(index + diff, index - diff, - 1):
                    del solution[ind]

        return solution
