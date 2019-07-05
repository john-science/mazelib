
from random import choice, shuffle
# If the code is not Cython-compiled, we need to add some imports.
try:
    from cython import compiled
except ModuleNotFoundError:
    compiled = False
if not compiled:
    from mazelib.solve.MazeSolveAlgo import MazeSolveAlgo


class ShortestPath(MazeSolveAlgo):
    """
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
                elif solutions[s][-1] != None:
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
            num_unfinished = sum(map(lambda sol: 0 if sol[-1] is None else 1 , solutions))

        # 4) clean-up solutions
        solutions = self._clean_up(solutions)

        if len(solutions) == 0 or len(solutions[0]) == 0:
            raise ValueError('No valid solutions found.')

        return solutions
