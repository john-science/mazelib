
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
        else:  # default to right tur
            self.directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]

    def solve(self, grid, start, end):
        # TODO: My pruning is not working correctly
        # TODO: I think it's possible my turn-around points are being skipped.
        # TODO: Code cleanup
        # TODO: Create _midpoint(a, b) method
        solution = []
        current = start

        # a first move has to be made
        if self._start_on_edge(start, grid):
            last = start
            current = self._push_edge_start(start, grid)
            solution.append(current)

        # pick a random direction
        last = current
        current = choice(self._find_neighbors(last, grid, False))
        
        solution.append(((last[0] + current[0]) // 2, (last[1] + current[1]) // 2))
        solution.append(current)

        limit = grid.height * grid.width
        last_diff = (current[0] - last[0], current[1] - last[1])
        last_dir = self.directions.index(last_diff)
        # loop until you reach end, or until you have proven you won't solve the maze
        while current != end and len(solution) < limit:
            last_dir,temp = self._move_to_next_cell(grid, last_dir, current, start, end)
            if temp == end:
                break
            solution.append(((temp[0] + current[0]) // 2, (temp[1] + current[1]) // 2))
            solution.append(temp)
            last = current
            current = temp

        if len(solution) >= limit:
            raise RuntimeError('This algorithm was not able to converge on a solution.')
            return []  # TODO: Is necessary?

        # remove unnecessary branches from the solution.
        solution = self._prune_solution(solution)

        return solution

    def _move_to_next_cell(self, grid, last_dir, current, start, end):
        """ At each new cell you reach, take the rightmost turn.
        Turn around if you reach a dead end.
        if right is not available, then straight, if not straight, left, etc...
        """
        for d in xrange(4):
            next_dir = (last_dir - 1 + d) % 4
            next_cell = self._move(current, self.directions[next_dir])
            mid_cell = ((next_cell[0] + current[0]) // 2, (next_cell[1] + current[1]) // 2)
            if grid[mid_cell] == 0 and mid_cell != start:
                return (next_dir, next_cell)
            elif mid_cell == end:
                return (next_dir, end)
        
        return (last_dir, current)

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
                del solution[index+2]
                del solution[index+1]
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

    def _start_on_edge(self, start, grid):
        """Does the starting cell lay on the edge, rather than the
        inside of the maze grid?
        """
        row,col = start
        
        if row == 0 or row == grid.height - 1:
            return True
        if col == 0 or col == grid.width - 1:
            return True

        return False

    def _push_edge_start(self, start, grid):
        """If you start on the edge of the maze,
        you need to push in one cell.
        
        This method assumes you start on the edge.
        """
        row,col = start
        
        if row == 0:
            return (1, col)
        elif row == (grid.height - 1):
            return (row - 1, col)
        elif col == 0:
            return (row, 1)
        else:
            return (row, col - 1)
