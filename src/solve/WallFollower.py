
from random import choice,shuffle
from MazeSolveAlgo import MazeSolveAlgo


class WallFollower(MazeSolveAlgo):
    """
    Ideally:
    
    0. Follow the right wall and you will eventually end up at the end.
    
    In reality:
    
    1. Choose a random starting direction.
    2. At each intersection, take the rightmost turn. At dead-ends, turn around.
    3. If you have gone more than (H * W) + 2 cells, stop; the maze will not be solved.
    4. Terminate when you reach the end cell.
    5. Prune the extraneous branches from the solution before returning it.
    """
    def __init__(self, turn='right'):
        if turn == 'right':
            self.directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]
        elif turn == 'left':
            self.directions = [(-2, 0), (0, -2), (2, 0), (0, 2)]
        else:  # default to right turns
            self.directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]

    def _solve(self):
        solution = []
        current = self.start

        # a first move has to be made
        if self._start_on_edge(self.start):
            current = self._push_edge_start(self.start)
            solution.append(current)

        # pick a random direction and move
        last = current
        current = choice(self._find_neighbors(last, False))
        last_diff = (current[0] - last[0], current[1] - last[1])
        last_dir = self.directions.index(last_diff)

        # add first move to solution
        solution.append(self._midpoint(last, current))
        solution.append(current)

        # loop until you have proven you won't solve the maze
        limit = self.grid.height * self.grid.width
        while len(solution) < limit:
            last_dir,temp = self._move_to_next_cell(last_dir, current)
            # the solution should not include the end point
            if temp == self.end:
                midpoint = self._midpoint(temp, current)
                if midpoint != self.end:
                    solution.append(midpoint)
                break
            solution.append(self._midpoint(temp, current))
            solution.append(temp)
            last = current
            current = temp

        if len(solution) >= limit:
            raise RuntimeError('This algorithm was not able to converge on a solution.')

        # remove unnecessary branches from the solution.
        solution = self._prune_solution(solution)

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

    def _start_on_edge(self, start):
        """Does the starting cell lay on the edge, rather than the
        inside of the maze grid?
        """
        row,col = start
        
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

    def _move(self, start, direction):
        """Convolve a position tuple with a direction tuple to
        generate a new position.
        """
        return tuple(map(sum, zip(start, direction)))

    def _midpoint(self, a, b):
        """Find the wall cell between to passage cells"""
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2
