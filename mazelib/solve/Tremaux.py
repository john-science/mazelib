
from random import choice
# If the code is not Cython-compiled, we need to add some imports.
try:
    from cython import compiled
except ModuleNotFoundError:
    compiled = False
if not compiled:
    from mazelib.solve.MazeSolveAlgo import MazeSolveAlgo


class Tremaux(MazeSolveAlgo):
    """
    1. When you hit a dead end turn around and go back.
    2. When you hit a junction you haven't visited, pick a new passage at random.
    3. If you're walking down a new passage and hit a junction you have visited,
        treat it like a dead end and go back.
    4. If walking down a passage you have visited before (i.e. marked once) and you hit a junction,
    take any new passage available, otherwise take an old passage (i.e. marked once).
    5. When you finally reach the end, follow cells marked exactly once back to the start.
    6. If the Maze has no solution, you'll find yourself at the start with all cells marked twice.

    Results

    Find one non-optimal solution.
    Works against imperfect mazes.

    Notes

    This Maze-solving method is designed to be used by a human inside the Maze.
    """
    def __init__(self):
        self.visited_coords = {}

    def _solve(self):
        raise Exception('This algorithm under development.')
        self.visited_coords = {}
        solution = []

        # a first move has to be made
        current = self.start
        if self._on_edge(self.start):
            current = self._push_edge(self.start)
        solution.append(current)
        self._visit(current)

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
            self._visit(nxt)

        # TODO: special pruning method, to backtrack through only cells marked with a '1'

        solution = self._fix_entrances(solution)

        return [solution]

    def _visit(self, cell):
        """Increment the number of times a cell has been visited."""
        if cell not in self.visited_coords:
            self.visited_coords[cell] = 1
        else:
            self.visited_coords[cell] += 1

    def _get_visit_count(self, cell):
        """How many times has a cell been visited?"""
        if cell not in self.visited_coords:
            return 0
        else:
            return self.visited_coords[cell]

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
