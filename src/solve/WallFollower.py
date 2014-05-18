
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
            self.directions = [(0, 2), (-2, 0), (0, -2), (2, 0)]
        elif turn == 'left':
            self.directions = [(0, -2), (-2, 0), (0, 2), (2, 0)]
        else:  # default to right turn
            self.directions = [(0, 2), (-2, 0), (0, -2), (2, 0)]

    def solve(self, grid, start, end):
        solution = []

        # a first move has to be made
        if self._start_on_edge(start):
            # push in one cell
        else:
            # pick a random direction
            last = start
            current = choice(self._find_neighbors(last, grid, False))

        limit = grid.height * grid.width + 2
        # loop until you reach end, or until you have proven you won't solve the maze
        while current != end and len(solution) < limit:
            temp = self._move_to_next_cell(grid, last, current)
            solution.append(temp)
            last = current
            current = temp

        if len(solution) > limit:
            raise RuntimeError('This algorithm was not able to converge on a solution.')
            return []  # TODO: Is necessary?

        # remove unnecessary branches from the solution.
        solution = self._prune_solution(solution)

        return solution

    def _move_to_next_cell(self, grid, last, current):
        """ At each new cell you reach, take the rightmost turn.
        Turn around if you reach a dead end.
        """
        last_diff = (current[0] - last[0], current[1] - last[1])
        last_dir = self.directions.index(last_diff)

        # loop through all directions until you find a place you can move
        for d in xrange(1,4):
            next_dir = (last_dir + d) % 4
            next_cell = self._move(current, self.directions[next_dir])
            # TODO: What if next_cell is outside of the maze??????
            if grid[next_cell] == 0:
                return next_cell

        # default to going back where you just came from
        return last

    def _move(self, start, direction):
        """Convolve a position tuple with a direction tuple to
        generate a new position.
        """
        return tuple(map(sum, zip(start, direction)))

    def _prune_solution(self, solution):
        """ A solution may contain extraneous branches: paths that were followed
        to find the end, but could have been skipped.
        This method removes those branches.
        """
        # remove all turn-around points in the solution
        found = True
        while found and len(solution) > 2:
            found = False
            for i in xrange(len(solution) - 2):
                if solution[i] == solution[i + 2]:
                    found = True
                    index = i + 1
                    break

            if found:
                del solution[index]

        # if the same row is listed twice in the solution, remove it
        found = True
        while found:
            found = False
            for i in xrange(len(solution) - 1):
                if solution[i] == solution[i + 1]:
                    found = True
                    index = i
                    break

            if found:
                del solution[index]

        return solution

    def _find_neighbors(self, posi, grid, visited=True):
        """Find all the grid neighbors of the current position;
        visited, or not.
        """
        (row, col) = posi
        ns = []

        if row > 1 and grid[row-2, col] == visited:
            ns.append((row-2, col))
        if row < grid.height-2 and grid[row+2, col] == visited:
            ns.append((row+2, col))
        if col > 1 and grid[row, col-2] == visited:
            ns.append((row, col-2))
        if col < grid.width-2 and grid[row, col+2] == visited:
            ns.append((row, col+2))

        shuffle(ns)

        return ns

    def _start_on_edge(self, start):
        row,col = start
        
        if row % 2 == 0:
            return False
        if col % 2 == 0:
            return False

        return True
