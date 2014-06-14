
from random import choice,shuffle
from MazeSolveAlgo import MazeSolveAlgo


class ShortestPaths(MazeSolveAlgo):
    """
    The Algorithm:

    1) create a solution for each starting position
    2) loop through each solution, and find the neighbors of the last element
    3) The first solution to reach the end wins.

    Results

    The shortest unique solutions. Works against imperfect mazes.
    """
    def _solve(self):
        # determine if edge or body entrances
        self.start_edge = self._on_edge(self.start)
        self.end_edge = self._on_edge(self.start)
        
        # a first move has to be made
        start = self.start
        if self.start_edge:
            start = self._push_edge(self.start)

        # find the starting positions
        start_posis = self._find_unblocked_neighbors(start)
        if len(start_posis) == 0:
            raise ValueError('Input maze is invalid.')
        
        # 1) create a solution for each starting position
        solutions = []
        for s in start_posis:
            if self.start_edge:
                solutions.append([start, self._midpoint(start, s), s])
            else:
                solutions.append([self._midpoint(start, s), s])

        # 2) loop through each solution, and find the neighbors of the last element
        num_unfinished = len(solutions)
        while num_unfinished > 0:
            for s in xrange(len(solutions)):
                if solutions[s][-1] in solutions[s][:-1]:
                    # stop all solutions that have done a full loop
                    solutions[s].append(None)
                elif self._within_one(solutions[s][-1], self.end):
                    # stop all solutions that have reached the end
                    solutions[s].append(None)
                elif solutions[s][-1] != None:
                    # continue with all un-stopped solutions
                    if len(solutions[s]) > 1:
                        # check to see if you've gone past the endpoint
                        if self._midpoint(solutions[s][-1], solutions[s][-2]) == self.end:
                            solutions[s].append(None)
                            continue

                    # find all the neighbors of the last cell in the solution
                    ns = self._find_unblocked_neighbors(solutions[s][-1])
                    ns = filter(lambda i: i not in solutions[s][-2:], ns)
                    
                    if len(ns) == 0:
                        # there are no valid neighbors
                        solutions[s].append(None)
                    elif len(ns) == 1:
                        # there is only one valid neighbor
                        solutions[s].append(self._midpoint(ns[0], solutions[s][-1]))
                        solutions[s].append(ns[0])
                    else:
                        # there are 2 or 3 valid neigbors
                        for j in xrange(1, len(ns)):
                            nxt = [self._midpoint(ns[j], solutions[s][-1]), ns[j]]
                            solutions.append(list(solutions[s]) + nxt)
                        solutions[s].append(self._midpoint(ns[0], solutions[s][-1]))
                        solutions[s].append(ns[0])

            # 3) a solution reaches the end or a dead end when we mark it by appending a None.
            num_unfinished = sum(map(lambda sol: 0 if sol[-1] is None else 1 , solutions))

        # 4) clean-up solutions
        solutions = self._clean_up(solutions)

        if len(solutions) == 0 or len(solutions[0]) == 0:
            raise ValueError('No valid solutions found.')

        return solutions
    
    def _clean_up(self, solutions):
        """Cleaning up the solutions in three stages:
        1) remove incomplete solutions
        2) remove duplicate solutions
        3) order the solutions by length (short to long)
        """
        # 1) remove incomplete solutions
        new_solutions = []
        for sol in solutions:
            new_sol = None
            if self.end_edge:
                last = self._push_edge(self.end)
                # remove edge-case end cells
                if len(sol) > 2 and self._within_one(sol[-2], self.end):
                    new_sol = sol[:-1]
                elif len(sol) > 2 and self._within_one(sol[-2], last):
                    new_sol = sol[:-1] + [last]
            else:
                # remove inside-maze-case end cells
                if len(sol) > 2 and self._within_one(sol[-2], self.end):
                    new_sol = sol[:-1]

            if new_sol:
                if new_sol[-1] == self.end:
                    new_sol = new_sol[:-1]
                new_solutions.append(self._prune_solution(new_sol))

        # 2) remove duplicate solutions
        solutions = self._remove_duplicate_sols(new_solutions)

        # order the solutions by length (short to long)
        solutions = sorted(solutions, key=len)

        return solutions

    def _prune_solution(self, sol):
        """In the process of solving a maze, the algorithm might go down
        the wrong corridor then backtrack.

        These extraneous branches need to be removed.
        """
        found = True
        while found and len(sol) > 2:
            found = False

            for i in xrange(1, len(sol) - 1):
                if sol[i - 1] != sol[i + 1]:
                    continue
                diff = 1

                while i-diff >= 0 and i+diff < len(sol) and sol[i-diff] == sol[i+diff]:
                    diff += 1
                diff -= 1
                index = i
                found = True
                break

            if found:
                for ind in xrange(index + diff, index - diff, - 1):
                    del sol[ind]

        # prune if start is found in solution
        if self.start in sol:
            i = sol.index(self.start)
            sol = sol[i+1:]
        # prune if first position is repeated
        if sol[0] in sol[1:]:
            i = sol[1:].index(sol[0])
            sol = sol[i+1:]
        # prune duplicate end points
        if len(sol) > 1 and sol[-2] == sol[-1]:
            sol = sol[:-1]

        return sol

    def _remove_duplicate_sols(self, sols):
        """Remove duplicate solutions using subsetting"""
        temp = list(set(map(tuple, sols)))
        return [list(s) for s in temp]

    def _find_unblocked_neighbors(self, cell):
        """Find all the grid neighbors of the current position,
        visited or not, that are not block by walls.
        """
        r,c = cell
        ns = []

        if r > 1 and not self.grid[r-1, c] and not self.grid[r-2, c]:
            ns.append((r-2, c))
        if r < self.grid.height-2 and not self.grid[r+1, c] and not self.grid[r+2, c]:
            ns.append((r+2, c))
        if c > 1 and not self.grid[r, c-1] and not self.grid[r, c-2]:
            ns.append((r, c-2))
        if c < self.grid.width-2 and not self.grid[r, c+1] and not self.grid[r, c+2]:
            ns.append((r, c+2))

        shuffle(ns)

        return ns

    def _push_edge(self, cell):
        """If you start or end on the edge of the maze,
        you need to push in one cell to be on the normal grid.
        """
        r,c = cell

        if r == 0:
            return (1, c)
        elif r == (self.grid.height - 1):
            return (r - 1, c)
        elif c == 0:
            return (r, 1)
        else:
            return (r, c - 1)

    def _on_edge(self, cell):
        """Determine is a cell is on the edge of the maze."""
        r,c = cell

        if r == 0 or r == (self.grid.height - 1):
            return True
        elif c == 0 or c == (self.grid.width - 1):
            return True

        return False

    def _midpoint(self, a, b):
        """Find the wall cell between to passage cells"""
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2

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
