from MazeSolveAlgo import MazeArray,MazeSolveAlgo


class WallFollower(MazeSolveAlgo):
    """
    1. Find the starting cell, pick an arbitrary direction to start in (not out of the maze)
    2. At each intersection, take the rightmost turn. At dead-ends, turn around.
    3. If you have gone more than (H * W) + 2 cells, stop; the maze will not be solved.
    4. Terminate when you reach the end cell.
    5. Prune the extraneous branches from the solution before returning it.
    """
    
    def solve(self, grid, start, end):
        solution = [current]

        # select a starting direction
        current = start
        # find neighbors and pick one
        # move there.
        
        limit = grid.height * grid.width + 2
        # loop until you reach end, or until you have proven you won't solve the maze
        while current != end and len(solution) < limit:
            # move to the next, rightmost, cell
            
        
        if len(solution) > limit:
            raise RuntimeError('This algorithm was not able to converge on a solution.')
            return []  # TODO: Is necessary?
        
        # remove unnecessary branches from the solution.
        solution = self._prune_solution(solution)
        
        return solution


    def _move_to_next_cell(self, grid, current):
        """ At each new cell you reach, take the rightmost turn.
        Turn around if you reach a dead end.
        """
        next = current
        
        # TODO
        
        return next

    def _prune_solution(self, solution):
        """ A solution may contain extraneous branches: paths that were followed
        to find the end, but could have been skipped.
        
        This method removes those branches.
        """
        
        # TODO
        
        return solution
