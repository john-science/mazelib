
from random import choice, shuffle
# If the code is not Cython-compiled, we need to add some imports.
try:
    from cython import compiled
except ModuleNotFoundError:
    compiled = False
if not compiled:
    from mazelib.solve.MazeSolveAlgo import MazeSolveAlgo


class ShortestPaths(MazeSolveAlgo):
    """
    1) create a solution for each starting position
    2) loop through each solution, and find the neighbors of the last element
    3) The first solution to reach the end wins.

    Results:

    The shortest unique solutions. Works against imperfect mazes.
    """

    def _solve(self):
        # determine if edge or body entrances
        self.start_edge = self._on_edge(self.start)
        self.end_edge = self._on_edge(self.end)

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
                    ns = [n for n in ns if n not in solutions[s][-2:]]

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

            for i in range(1, len(sol) - 1):
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
                for ind in range(index + diff, index - diff, - 1):
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
        """ Remove duplicate solutions using subsetting """
        return [list(s) for s in set(map(tuple, sols))]
