
from random import choice,shuffle
from MazeSolveAlgo import MazeSolveAlgo


class DeadEndFiller(MazeSolveAlgo):
    """
    This is a simple Maze solving algorithm.
    It focuses on the Maze, is always very fast, and uses no extra
    memory.

    Just scan the Maze, and fill in each dead end, filling in the
    passage backwards from the block until you reach a junction. This
    includes filling in passages that become parts of dead ends once
    other dead ends are removed. At the end only the solution will
    remain, or solutions if there are more than one.
    
    What is left is a maze with only solution tiles. Loop through
    these cells and build the solution(s).

    This will always find the one unique solution for perfect Mazes,
    but won't do much in heavily braid Mazes, and in fact won't do
    anything useful at all for those Mazes without dead ends.
    """
    def _solve(self):
        self.grid[self.start] = self.grid[self.end] = 0
        current = self.start

        # loop through the maze serpentine, and find dead ends
        dead_end = self._find_dead_end()
        while dead_end != (-1, -1):
            # from the dead end, travel one cell.
            ns = self._find_neighbors(dead_end)

            # fill-in and wall-off the dead end
            self._fill_dead_end(dead_end)

            # look at the next cell, if it is a dead end, restart the loop
            if len(ns) == 1:
                # continue until you are in a junction cell.
                if self._is_dead_end(ns[0]):
                    dead_end = ns[0]
                    continue

            # otherwise, find another dead end in the maze
            dead_end = self._find_dead_end(s)

        solutions = self._build_solutions()
       
        return solutions
    
    def _build_solutions(self):
        """The maze generated has only solution cells.
        But the maze may have more than one solution. These need to be sorted out.
        """
        # TODO: Will this be shared with other solvers?
        
        # find the starting positions
        start_posis = self._find_neighbors(self.start)
        
        if len(start_posis) == 0:
            raise ValueError('No valid solutions found.')
        
        # 0. start a solution at each starting position
        solutions = []
        for s in start_posis:
            solutions.append([s])
        
        num_unfinished = len(solutions)
        # 1. loop through each solution, and find the neighbors of the last element
        while num_unfinished > 0:
            for s in len(solutions):
                if solutions[s][-1] in solutions[s][:-1]:
                    solutions[s].append(None)
                elif solutions[s][-1] == start.end:
                    solutions[s].append(None)
                elif solutions[s][-1] != None:
                    # 2. since there are no dead ends, there can be 2, 3, or 4 neighbors
                    ns = self._find_neighbors(solutions[s][-1])
                    if len(ns) in [0, 1]:
                        solutions[s].append(None)
                    # 3. if 2, add the new cell to the colution
                    elif len(ns) == 2:
                        if ns[0] == solutions[s][-1]:
                            solutions[s].append(ns[1])
                        else:
                            solutions[s].append(ns[0])
                    # 4. if 3 or 4, 1 or 2 new solutions must be generated
                    else:
                        ns.remove(solutions[s][-1])
                        solutions[s].append(ns[0])
                        for j in xrange(1, len(ns)):
                            solutions.append(list(solutions[s]).append(ns[j]))
            
            # 5. a solution is done when we mark it by appending a None.
            num_unfinished = sum(map(lambda sol: 0 if sol[-1] is None else 1 , solutions))
                            
        # 6. clean-up: remove incomplete solutions
        new_solutions = []
        for sol in solutions:
            if len(sol) > 2 and sol[-1] = start.end:
                # remove end cell from solution
                new_solutions.append(sol[:-2])
                
        # 7. clean-up: organize solutions by length
        solutions = sorted(new_solutions, key=len)
        
        if len(solutions) == 0 or len(solutions[0]) == 0:
            raise ValueError('No valid solutions found.')

        return solutions

    def _fill_dead_end(self, dead_end):
        """After moving from a dead end, we want to fill in it and all
        the walls around it.
        """
        r,c = dead_end
        grid[r, c] = 1
        grid[r - 1, c] = 1
        grid[r + 1, c] = 1
        grid[r, c - 1] = 1
        grid[r, c + 1] = 1

    def _find_dead_end(self):
        """A "dead end" is a cell with only zero or one open neighbors.
        The start end end count as open.
        """
        for r in xrange(1, self.grid.height, 2):
            for c in xrange(1, self.grid.width, 2):
                if (n, c) in [self.start, self.end]:
                    continue
                if self._is_dead_end((r, c)):
                    return (r, c)

        return (-1, -1)

    def _is_dead_end(self, cell):
        """A dead end has zero or one open neighbors."""
        ns = self._find_neighbors(cell)
        if len(ns) in [0, 1]:
            return True
        else:
            return False

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
