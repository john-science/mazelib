
from random import choice,shuffle
from MazeSolveAlgo import MazeSolveAlgo


class ShortestPath(MazeSolveAlgo):
    """
    The Algorithm:

    1) create a solution for each starting position
    2) loop through each solution, and find the neighbors of the last element
    3) a solution reaches the end or a dead end when we mark it by appending a None.
    4) clean-up solutions

    Results

    Find all unique solutions. Works against imperfect mazes.
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
                    return [solutions[s]]
                elif solutions[s][-1] != None:
                    # continue with all un-stopped solutions
                    if len(solutions[s]) > 1:
                        # check to see if you've gone past the endpoint
                        if self._midpoint(solutions[s][-1], solutions[s][-2]) == self.end:
                            return [solutions[s][:-1]]

                    # find all the neighbors of the last cell in the solution
                    ns = self._find_unblocked_neighbors(solutions[s][-1])
                    if len(ns) in [0, 1]:
                        # there are no valid neighbors
                        solutions[s].append(None)
                    elif len(ns) == 2:
                        # there is only one valid neighbor
                        if ns[0] in solutions[s] or ns[0] == self.start:
                            i = 1
                        else:
                            i = 0
                        solutions[s].append(self._midpoint(ns[i], solutions[s][-1]))
                        solutions[s].append(ns[i])
                    else:
                        # there are 2 or 3 valid neigbors
                        if len(solutions[s]) > 2 and solutions[s][-3] in ns:
                            ns.remove(solutions[s][-3])

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

    def _remove_dup_sols(self, sols):
        """Remove duplicate solutions using subsetting"""
        uniques = []
        solsets = [set(s) for s in sols]
        for i,sol in enumerate(solsets):
            unique = True
            for j,sol2 in enumerate(solsets[:i] + solsets[i+1:]):
                if sol.issuperset(sol2):
                    unique = False
                    break

            if unique:
                uniques.append(sols[i])

        return uniques

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
