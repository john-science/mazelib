
from random import choice
import cython
if not cython.compiled:
    from mazelib.solve.MazeSolveAlgo import MazeSolveAlgo


class RandomMouse(MazeSolveAlgo):
    """
    The Algorithm

    A mouse just randomly wanders around the maze until it finds the cheese.
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

            nxt = choice(ns)
            solution.append(self._midpoint(solution[-1], nxt))
            solution.append(nxt)

        if self.prune:
            solution = self._prune_solution(solution)

        solution = self._fix_entrances(solution)

        return [solution]

    def _move_to_next_cell(self, last_dir, current):
        """ At each new cell you reach, take the rightmost turn.
        Turn around if you reach a dead end.
        if right is not available, then straight, if not straight, left, etc...
        """
        for d in range(4):
            next_dir = (last_dir - 1 + d) % 4
            next_cell = self._move(current, self.directions[next_dir])
            r, c = (self._midpoint(next_cell, current))

            if self.grid[r, c] == 0 and (r, c) != self.start:
                return (next_dir, next_cell)
            elif (r, c) == self.end:
                return (next_dir, self.end)

        return (last_dir, current)

    def _fix_entrances(self, solution):
        """Ensure the start and end are appropriately placed in the solution."""
        # prune if start is found in solution
        if self.start in solution:
            i = solution.index(self.start)
            solution = solution[i+1:]

        # prune if end is found in solution
        if self.end in solution:
            i = solution.index(self.end)
            solution = solution[:i]


        # fix solution so it doesn't overlap endpoints
        #if not self._on_edge(self.end):
        #    solution = solution[:-1]

        return solution
