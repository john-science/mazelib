from random import choice
# If the code is not Cython-compiled, we need to add some imports.
from cython import compiled
if not compiled:
    from mazelib.solve.MazeSolveAlgo import MazeSolveAlgo


class RandomMouse(MazeSolveAlgo):
    """ This mouse just randomly wanders around the maze until it finds the cheese. """

    def _solve(self):
        """ Solve a maze as stupidly as possible: just wander randomly until you find the end.
        This should be basically optimally slow and should have just obsurdly long solutions,
        with lots of double backs.

        Returns:
            list: solution to the maze
        """
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

        return [solution]