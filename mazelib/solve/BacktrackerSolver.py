from random import choice,shuffle
from MazeSolveAlgo import MazeSolveAlgo


class BacktrackerSolver(MazeSolveAlgo):
    """
    The Algorithm

    TODO
    """
    def _solve(self):
        solution = []

        # a first move has to be made
        current = self.start
        if self._on_edge(self.start):
            current = self._push_edge_start(self.start)
        solution.append(current)

        # pick a random neighbor and travel to it, until you're at the end
        while not self._within_one(solution[-1], self.end):
            ns = self._find_unblocked_neighbors(solution[-1])

            if len(ns) > 1 and len(solution) > 2:
                del ns[solution[-3]]

            nxt = choice(ns)
            solution.append(self._midpoint(solution[-1], nxt))
            solution.append(nxt)

        # remove unnecessary branches from the solution.
        solution = self._prune_solution(solution)

        # fix solution so it doesn't overlap endpoints
        if not self._on_edge(self.end):
            [solution] = [solution[:-1]]

        return [solution]

    def _move_to_next_cell(self, last_dir, current):
        """ At each new cell you reach, take the rightmost turn.
        Turn around if you reach a dead end.
        if right is not available, then straight, if not straight, left, etc...
        """
        for d in xrange(4):
            next_dir = (last_dir - 1 + d) % 4
            next_cell = self._move(current, self.directions[next_dir])
            mid_cell = (self._midpoint(next_cell, current))

            if self.grid[mid_cell] == 0 and mid_cell != self.start:
                return (next_dir, next_cell)
            elif mid_cell == self.end:
                return (next_dir, self.end)

        return (last_dir, current)

    def _find_unblocked_neighbors(self, posi):
        """Find all the grid neighbors of the current position;
        visited, or not.
        """
        (row, col) = posi
        ns = []

        if row > 1 and self.grid[row-1, col] == False and self.grid[row-2, col] == False:
            ns.append((row-2, col))
        if row < self.grid.height-2 and self.grid[row+1, col] == False and self.grid[row+2, col] == False:
            ns.append((row+2, col))
        if col > 1 and self.grid[row, col-1] == False and self.grid[row, col-2] == False:
            ns.append((row, col-2))
        if col < self.grid.width-2 and self.grid[row, col+1] == False and self.grid[row, col+2] == False:
            ns.append((row, col+2))

        shuffle(ns)

        return ns

    def _prune_solution(self, solution):
        """In the process of solving a maze, the algorithm might go down
        the wrong corridor then backtrack.

        These extraneous branches need to be removed.
        """
        # TODO: Will this be shared with other solvers?
        # prune extra branches
        found = True
        while found and len(solution) > 2:
            found = False

            for i in xrange(1, len(solution) - 1):
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
                for ind in xrange(index + diff, index - diff, - 1):
                    del solution[ind]

        # prune if start is found in solution
        if self.start in solution:
            i = solution.index(self.start)
            solution = solution[i+1:]

        return solution

    def _on_edge(self, cell):
        """Does the cell lay on the edge, rather inside of the maze grid?"""
        r,c = cell

        if r == 0 or r == self.grid.height - 1:
            return True
        if c == 0 or c == self.grid.width - 1:
            return True

        return False

    def _push_edge_start(self, start):
        """If you start on the edge of the maze,
        you need to push in one cell.
        This method assumes you start on the edge.
        """
        row,col = start

        if row == 0:
            return (1, col)
        elif row == (self.grid.height - 1):
            return (row - 1, col)
        elif col == 0:
            return (row, 1)
        else:
            return (row, col - 1)

    def _move(self, start, direction):
        """Convolve a position tuple with a direction tuple to
        generate a new position.
        """
        return tuple(map(sum, zip(start, direction)))

    def _midpoint(self, a, b):
        """Find the wall cell between to passage cells"""
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2

    def _within_one(self, cell, desire):
        """Is the current cell within one move of the desired cell?
        Note, this might be one full more, or one half move.
        """
        if not cell or not desire:
            return False

        rdiff = abs(cell[0] - desire[0])
        cdiff = abs(cell[1] - desire[1])

        if rdiff == 0 and cdiff < 2:
            return True
        elif cdiff == - and rdiff < 2:
            return True

        return False
