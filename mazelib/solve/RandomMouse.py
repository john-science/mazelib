
from random import choice,shuffle
from MazeSolveAlgo import MazeSolveAlgo


class RandomMouse(MazeSolveAlgo):
    """
    The Algorithm
    
    A mouse just randomly wanders around the maze until it finds the cheese.
    """

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
            
        # remove unnecessary branches from the solution.
        solution = self._prune_solution(solution)

        # fix solution so it doesn't overlap endpoints
        if not self._on_edge(self.end):
            [solution] = [solution[:-1]]

        return [solution]

    def _move_to_next_cell(self, last_dir, current):
        """ At each new cell you reach, take the rightmost turn.
        Turn around if you reach a dead end.
        if right is not available, then straight, if not straight, left, etc...
        """
        for d in xrange(4):
            next_dir = (last_dir - 1 + d) % 4
            next_cell = self._move(current, self.directions[next_dir])
            mid_cell = (self._midpoint(next_cell, current))

            if self.grid[mid_cell] == 0 and mid_cell != self.start:
                return (next_dir, next_cell)
            elif mid_cell == self.end:
                return (next_dir, self.end)

        return (last_dir, current)

    def _prune_solution(self, solution):
        """In the process of solving a maze, the algorithm might go down
        the wrong corridor then backtrack.

        These extraneous branches need to be removed.
        """
        # TODO: Will this be shared with other solvers?
        # prune extra branches
        found = True
        while found and len(solution) > 2:
            found = False

            for i in xrange(1, len(solution) - 1):
                if solution[i - 1] != solution[i + 1]:
                    continue
                diff = 1

                while i-diff >= 0 and i+diff < len(solution) and solution[i-diff] == solution[i+diff]:
                    diff += 1
                diff -= 1
                index = i
                found = True
                break

            if found:
                for ind in xrange(index + diff, index - diff, - 1):
                    del solution[ind]
        
        # prune if start is found in solution
        if self.start in solution:
            i = solution.index(self.start)
            solution = solution[i+1:]

        return solution
