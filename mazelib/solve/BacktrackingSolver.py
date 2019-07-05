
from random import choice
# If the code is not Cython-compiled, we need to add some imports.
try:
    from cython import compiled
except ModuleNotFoundError:
    compiled = False
if not compiled:
    from mazelib.solve.MazeSolveAlgo import MazeSolveAlgo


class BacktrackingSolver(MazeSolveAlgo):
    """
    1. Pick a random direction and follow it
    2. Backtrack if and only if you hit a dead end.
    """
    def __init__(self, prune=True):
        self.prune = prune

    def _solve(self):
        solution = []

        # a first move has to be made
        current = self.start
        if self._on_edge(self.start):
            current = self._push_edge(self.start)
        solution.append(current)

        # pick a random neighbor and travel to it, until you're at the end
        while not self._within_one(solution[-1], self.end):
            ns = self._find_unblocked_neighbors(solution[-1])

            # do no go where you've just been
            if len(ns) > 1 and len(solution) > 2:
                if solution[-3] in ns:
                    ns.remove(solution[-3])

            nxt = choice(ns)
            solution.append(self._midpoint(solution[-1], nxt))
            solution.append(nxt)

        if self.prune:
            solution = self._prune_solution(solution)

        solution = self._fix_entrances(solution)

        return [solution]

    def _fix_entrances(self, solution):
        """Ensure the start and end are appropriately placed in the solution."""
        # prune if start is found in solution
        if self.start in solution:
            i = solution.index(self.start)
            solution = solution[i+1:]

        # fix solution so it doesn't overlap endpoints
        if not self._on_edge(self.end):
            [solution] = [solution[:-1]]

        return solution
