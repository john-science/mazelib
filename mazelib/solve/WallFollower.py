
from random import choice, shuffle
# If the code is not Cython-compiled, we need to add some imports.
try:
    from cython import compiled
except ModuleNotFoundError:
    compiled = False
if not compiled:
    from mazelib.solve.MazeSolveAlgo import MazeSolveAlgo


class WallFollower(MazeSolveAlgo):
    """
    Follow the right wall and you will eventually end up at the end.

    details:

    1. Choose a random starting direction.
    2. At each intersection, take the rightmost turn. At dead-ends, turn around.
    3. If you have gone more than (H * W) + 2 cells, stop; the maze will not be solved.
    4. Terminate when you reach the end cell.
    5. Prune the extraneous branches from the solution before returning it.

    Optional Parameters

    Turn: String ['left', 'right']
        Do you want to follow the right wall or the left wall? (default 'right')
    """

    def __init__(self, turn='right', prune=True):
        # turn can take on values 'left' or 'right'
        if turn == 'left':
            self.directions = [(-2, 0), (0, -2), (2, 0), (0, 2)]
        else:  # default to right turns
            self.directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]

        self.prune = prune

    def _solve(self):
        solution = []
        current = self.start

        # a first move has to be made
        if self._on_edge(self.start):
            current = self._push_edge(self.start)
            solution.append(current)

        # pick a random direction and move
        last = current
        current = choice(self._find_neighbors(last, False))
        last_diff = (current[0] - last[0], current[1] - last[1])
        last_dir = self.directions.index(last_diff)

        # add first move to solution
        solution.append(self._midpoint(last, current))
        solution.append(current)

        # now that you have set up the situation, follow the walls
        solution = self._follow_walls(last_dir, current, solution)

        if self.prune:
            solution = self._prune_solution(solution)

        solution = self._fix_entrances(solution)

        return [solution]

    def _follow_walls(self, last_dir, current, solution):
        """ Perform the wall following logic.
        Loop until you have found the end,
        or prove you won't solve the maze.
        """
        limit = self.grid.shape[0] * self.grid.shape[1] + 2

        while len(solution) < limit:
            last_dir, temp = self._follow_one_step(last_dir, current)
            # the solution should not include the end point
            if temp == self.end:
                midpoint = self._midpoint(temp, current)
                if midpoint != self.end:
                    solution.append(midpoint)
                break
            solution.append(self._midpoint(temp, current))
            solution.append(temp)
            current = temp

        if len(solution) >= limit:
            raise RuntimeError('{0} can only solve perfect mazes - '.format(self.__class__.__name__) +
                'it can not solve mazes with loops.')

        return solution

    def _follow_one_step(self, last_dir, current):
        """ At each new cell you reach, take the rightmost turn.
        Turn around if you reach a dead end.
        if right is not available, then straight, if not straight, left, etc...
        """
        for d in range(4):
            next_dir = (last_dir - 1 + d) % 4
            next_cell = self._move(current, self.directions[next_dir])
            r, c= self._midpoint(next_cell, current)

            if self.grid[r, c] == 0 and (r, c) != self.start:
                return (next_dir, next_cell)
            elif (r, c) == self.end:
                return (next_dir, self.end)

        return (last_dir, current)

    def _fix_entrances(self, solution):
        """ Ensure the start and end are appropriately placed in the solution. """
        # prune if start is found in solution
        if self.start in solution:
            i = solution.index(self.start)
            solution = solution[i+1:]

        # prune if first position is repeated
        if solution[0] in solution[1:]:
            i = solution[1:].index(solution[0])
            solution = solution[i+1:]

        # prune duplicate end points
        if len(solution) > 1 and solution[-2] == solution[-1]:
            solution = solution[:-1]

        return solution
