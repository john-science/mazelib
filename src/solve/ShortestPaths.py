
from random import choice,shuffle
from MazeSolveAlgo import MazeSolveAlgo


class ShortestPaths(MazeSolveAlgo):
    """
    In CS terms, this is a Breadth-First Search algorithm.
    It finds all unique, non-looped solutions to the maze.
    """
    def _solve(self):
        raise NotImplementedError('This algorithm is incomplete.')
       
        # find the starting positions
        start_posis = self._find_neighbors(self.start)
        
        if len(start_posis) == 0:
            raise ValueError('Input maze is invalid.')
        
        # 0. start a solution at each starting position
        solutions = []
        
        for s in start_posis:
            solutions.append([s])
        
        # TODO: All of the self.end below are wrong. What if it is an edge start/end?
        
        num_unfinished = len(solutions)
        # 1. loop through each solution, and find the neighbors of the last element
        while num_unfinished > 0:
            print(num_unfinished)
            for s in xrange(len(solutions)):
                if solutions[s][-1] in solutions[s][:-1]:
                    solutions[s].append(None)
                elif self._within_one(solutions[s][-1], self.end):
                    solutions[s].append(None)
                elif solutions[s][-1] != None:
                    if len(solutions[s]) > 1:
                        # TODO: Document this: just a check to see if you've gone past the endpoint
                        if self._midpoint(solutions[s][-1], solutions[s][-2]) == self.end:
                            solutions[s].append(None)
                            continue
                    # 2. since there are no dead ends, there can be 2, 3, or 4 neighbors
                    ns = self._find_unblocked_neighbors(solutions[s][-1])
                    if len(ns) in [0, 1]:
                        solutions[s].append(None)
                    # 3. if 2 neighbors, add the new cell to the colution
                    elif len(ns) == 2:
                        # TODO: Is this logic sound? What about the first move? Will the last cell always be in ns?
                        # TODO: Review this logic. If we are at a dead-end, what happens?
                        if len(solutions[s]) > 1 and ns[0] == solutions[s][-2]:
                            solutions[s].append(self._midpoint(ns[1], solutions[s][-1]))
                            solutions[s].append(ns[1])
                        else:
                            solutions[s].append(self._midpoint(ns[0], solutions[s][-1]))
                            solutions[s].append(ns[0])
                    # 4. if 3 or 4, 1 or 2 new solutions must be generated
                    else:
                        # TODO: Review this logic. If we are at a dead-end, what happens?
                        if len(solutions[s]) > 1:
                            ns.remove(solutions[s][-3])
                        
                        for j in xrange(1, len(ns)):
                            if ns[j] not in solutions[s]:  # TODO: Necessary?
                                solutions.append(list(solutions[s]) + [self._midpoint(ns[j], solutions[s][-1]), ns[j]])
                        solutions[s].append(self._midpoint(ns[0], solutions[s][-1]))
                        solutions[s].append(ns[0])

            # 5. a solution is done when we mark it by appending a None.
            num_unfinished = sum(map(lambda sol: 0 if sol[-1] is None else 1 , solutions))

        # 6. clean-up: remove incomplete solutions
        new_solutions = []
        for sol in solutions:
            if len(sol) > 2 and sol[-2] == self.end:
                # remove end cell from solution
                new_solutions.append(sol[:-2])
                
        # 7. clean-up: organize solutions by length
        solutions = sorted(new_solutions, key=len)
        
        if len(solutions) == 0 or len(solutions[0]) == 0:
            print self.start, self.end
            raise ValueError('No valid solutions found.')

        return solutions

    def _fill_dead_end(self, dead_end):
        """After moving from a dead end, we want to fill in it and all
        the walls around it.
        """
        r,c = dead_end
        self.grid[r, c] = 1
        self.grid[r - 1, c] = 1
        self.grid[r + 1, c] = 1
        self.grid[r, c - 1] = 1
        self.grid[r, c + 1] = 1

    def _find_dead_end(self):
        """A "dead end" is a cell with only zero or one open neighbors.
        The start end end count as open.
        """
        for r in xrange(1, self.grid.height, 2):
            for c in xrange(1, self.grid.width, 2):
                if (r, c) in [self.start, self.end]:
                    continue
                if self._is_dead_end((r, c)):
                    return (r, c)

        return (-1, -1)

    def _is_dead_end(self, cell):
        """A dead end has zero or one open neighbors."""
        ns = self._find_neighbors(cell)
        if self.grid[cell] == 1:
            return False
        elif len(ns) in [0, 1]:
            return True
        else:
            return False

    def _find_unblocked_neighbors(self, posi, visited=True):
        """Find all the grid neighbors of the current position;
        visited, or not.
        """
        (row, col) = posi
        ns = []

        if row > 1 and self.grid[row-1, col] != visited and self.grid[row-2, col] != visited:
            ns.append((row-2, col))
        if row < self.grid.height-2 and self.grid[row+1, col] and self.grid[row+2, col] != visited:
            ns.append((row+2, col))
        if col > 1 and self.grid[row, col-1] and self.grid[row, col-2] != visited:
            ns.append((row, col-2))
        if col < self.grid.width-2 and self.grid[row, col+1] and self.grid[row, col+2] != visited:

            ns.append((row, col+2))

        shuffle(ns)

        return ns

    def _find_neighbors(self, posi, visited=True):
        """Find all the grid neighbors of the current position;
        visited, or not.
        """
        (row, col) = posi
        ns = []

        if row > 1 and self.grid[row-2, col] != visited:
            ns.append((row-2, col))
        if row < self.grid.height-2 and self.grid[row+2, col] != visited:
            ns.append((row+2, col))
        if col > 1 and self.grid[row, col-2] != visited:
            ns.append((row, col-2))
        if col < self.grid.width-2 and self.grid[row, col+2] != visited:

            ns.append((row, col+2))

        shuffle(ns)

        return ns

    def _start_on_edge(self):
        """Does the starting cell lay on the edge, rather than the
        inside of the maze grid?
        """
        row,col = self.start

        if row == 0 or row == self.grid.height - 1:
            return True
        if col == 0 or col == self.grid.width - 1:
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
