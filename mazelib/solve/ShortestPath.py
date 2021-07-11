# If the code is not Cython-compiled, we need to add some imports.
from cython import compiled
if not compiled:
    from mazelib.solve.MazeSolveAlgo import MazeSolveAlgo


class ShortestPath(MazeSolveAlgo):
    """ The Algorithm

    1) create a solution for each starting position
    2) loop through each solution, and find the neighbors of the last element
    3) a solution reaches the end or a dead end when we mark it by appending a None.
    4) clean-up solutions

    Results

    Find all unique solutions. Works against imperfect mazes.
    """

    def _solve(self):
        """ bredth-first search solution to the maze

        Returns:
            list: valid maze solutions
        """
        # determine if edge or body entrances
        self.start_edge = self._on_edge(self.start)
        self.end_edge = self._on_edge(self.start)

        # a first move has to be made
        start = self.start
        if self.start_edge:
            start = self._push_edge(self.start)

        # find the starting positions
        start_posis = self._find_unblocked_neighbors(start)
        assert len(start_posis) > 0, 'Input maze is invalid.'

        # 1) create a solution for each starting position
        solutions = []
        for sp in start_posis:
            if self.start_edge:
                solutions.append([start, self._midpoint(start, sp), sp])
            else:
                solutions.append([self._midpoint(start, sp), sp])

        # 2) loop through each solution, and find the neighbors of the last element
        num_unfinished = len(solutions)
        while num_unfinished > 0:
            for s in range(len(solutions)):
                if solutions[s][-1] in solutions[s][:-1]:
                    # stop all solutions that have done a full loop
                    solutions[s].append(None)
                elif self._within_one(solutions[s][-1], self.end):
                    # stop all solutions that have reached the end
                    if not self._on_edge(self.end):
                        # fix solution so it doesn't overlap endpoints
                        solutions[s] = solutions[s][:-1]
                    return [solutions[s]]
                elif solutions[s][-1] is not None:
                    # continue with all un-stopped solutions
                    if len(solutions[s]) > 1:
                        # check to see if you've gone past the endpoint
                        if self._midpoint(solutions[s][-1], solutions[s][-2]) == self.end:
                            return [solutions[s][:-1]]

                    # find all the neighbors of the last cell in the solution
                    ns = self._find_unblocked_neighbors(solutions[s][-1])
                    ns = [n for n in ns if n not in solutions[s]]

                    if len(ns) == 0:
                        # there are no valid neighbors
                        solutions[s].append(None)
                    elif len(ns) == 1:
                        # there is only one valid neighbor
                        solutions[s].append(self._midpoint(ns[0], solutions[s][-1]))
                        solutions[s].append(ns[0])
                    else:
                        # there are 2 or 3 valid neigbors
                        for j in range(1, len(ns)):
                            nxt = [self._midpoint(ns[j], solutions[s][-1]), ns[j]]
                            solutions.append(list(solutions[s]) + nxt)
                        solutions[s].append(self._midpoint(ns[0], solutions[s][-1]))
                        solutions[s].append(ns[0])

            # 3) a solution reaches the end or a dead end when we mark it by appending a None.
            num_unfinished = sum(map(lambda sol: 0 if sol[-1] is None else 1, solutions))

        # 4) clean-up solutions
        solutions = self._clean_up(solutions)

        assert (len(solutions) > 0 and len(solutions[0]) > 0), 'No valid solutions found.'

        return solutions

    def _clean_up(self, solutions):
        """ Cleaning up the solutions in three stages:
        1) remove incomplete solutions
        2) remove duplicate solutions
        3) order the solutions by length (short to long)

        Args:
            solutions (list): collection of maze solutions
        Returns:
            list: cleaner collection of solutions
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
                new_solutions.append(new_sol)

        # 2) remove duplicate solutions
        solutions = self._remove_duplicate_sols(new_solutions)

        # order the solutions by length (short to long)
        return sorted(solutions, key=len)

    def _remove_duplicate_sols(self, sols):
        """ Remove duplicate solutions using subsetting

        Args:
            solutions (list): collection of maze solutions
        Returns:
            list: collection of unique maze solutions
        """
        return [list(s) for s in set(map(tuple, sols))]
