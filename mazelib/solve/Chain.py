
# If the code is not Cython-compiled, we need to add some imports.
try:
    from cython import compiled
except ModuleNotFoundError:
    compiled = False
if not compiled:
    from mazelib.solve.MazeSolveAlgo import MazeSolveAlgo


class Chain(MazeSolveAlgo):
    """
    1. draw a straight-ish line from start to end, ignore the walls.
    2. Follow the line from start to end.
        a. If you bump into a wall, you have to go around.
        b. Send out wall-following robots in the 1 or 2 open directions.
        c. If the robot can find your new point, continue on.
        d. If the robot intersects your line at a point that is further down stream,
            pick up the path there.
    3. repeat step 2 until you are at the end.
        a. If both robots return to their original location and direction,
            the maze is unsolvable.
    """
    def __init__(self, turn='right', prune=True):
        # turn can take on values 'left' or 'right'
        if turn == 'left':
            self.directions = [(-2, 0), (0, -2), (2, 0), (0, 2)]
        else:  # default to right turns
            self.directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]

        self.prune = prune

    def _solve(self):
        guiding_line = self._draw_guiding_line()

        current = 0
        solution = [guiding_line[0]]
        len_guiding_line = len(guiding_line)

        while current < len_guiding_line - 1:
            # try to move to the next location
            success = self._try_direct_move(solution, guiding_line, current)
            if success:
                current += 1
            else:
                current = self._send_out_robots(solution, guiding_line, current)

        if self.prune:
            solution = self._prune_solution(solution)

        solution = self._fix_entrances(solution)

        return [solution]

    def _send_out_robots(self, solution, guiding_line, i):
        """ send out wall-following robots in all directions,
            to look for the next point in the guiding line
        """
        ns = self._find_unblocked_neighbors(guiding_line[i])

        # create a robot for each open neighbor
        robot_paths = []
        for n in ns:
            robot_path = []
            robot_path.append(guiding_line[i])
            robot_path.append(self._midpoint(guiding_line[i], n))
            robot_path.append(n)
            robot_paths.append(robot_path)

        # randomly walk each robot, until it finds the guiding line or dies
        for j, path in enumerate(robot_paths):
            last_diff = (path[-1][0] - path[-3][0], path[-1][1] - path[-3][1])
            last_dir = self.directions.index(last_diff)
            robot_paths[j] = self._follow_walls(last_dir, path[-1], path, guiding_line[i+1:])

        # if all robots return, the maze is unsolvable
        robot_paths = [p for p in robot_paths if p is not None]

        if len(robot_paths) == 0:
            raise Exception('No valid solution found.')

        # add the shortest path to the solution
        shortest_robot_path = robot_paths[0]
        min_len = len(shortest_robot_path)
        for j, path in enumerate(robot_paths[1:]):
            if len(path) < min_len:
                shortest_robot_path = path
                min_len = len(path)
        solution += shortest_robot_path[1:]

        return guiding_line.index(solution[-1])

    def _has_robot_returned(self, first_dir, path):
        """ Has the robot return to the same position and direction as it started? """
        if len(path) < 4:
            return False

        last_diff = (path[-1][0] - path[-3][0], path[-1][1] - path[-3][1])
        last_dir = self.directions.index(last_diff)

        if last_dir == first_dir and path[-1] == path[0]:
            return True

        return False

    def _follow_walls(self, last_dir, current, solution, goal):
        """ Perform the wall following logic.
        Loop until you have found the end,
        or prove you won't solve the maze.
        """
        path = list(solution)
        first_diff = (path[2][0] - path[0][0], path[2][1] - path[0][1])
        first_dir = self.directions.index(first_diff)

        while not self._has_robot_returned(first_dir, solution):
            last_dir,temp = self._follow_one_step(last_dir, current)
            # if you get further down stream than you expect, good
            if temp in goal:
                path.append(self._midpoint(temp, current))
                path.append(temp)
                break
            path.append(self._midpoint(temp, current))
            path.append(temp)
            current = temp

        if self._has_robot_returned(first_dir, solution):
            return None

        return path

    def _follow_one_step(self, last_dir, current):
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

        return (last_dir, current)

    def _try_direct_move(self, solution, guiding_line, i):
        """ The path to the next spot on the guiding line might be open.
            If so, add a couple steps to the solution.
            If not, return False.
        """
        r, c = guiding_line[i]
        next = guiding_line[i + 1]

        rdiff = next[0] - r
        cdiff = next[1] - c

        if rdiff == 0:
            if self.grid[r, c + cdiff//2] == 0:
                solution.append((r, c + cdiff//2))
                solution.append((r, c + cdiff))
                return True
        elif cdiff == 0:
            if self.grid[r + rdiff//2, c] == 0:
                solution.append((r + rdiff//2, c))
                solution.append((r + rdiff, c))
                return True
        else:
            if self.grid[r + rdiff//2, c] == 0 and self.grid[r + rdiff, c + cdiff//2] == 0:
                solution.append((r + rdiff//2, c))
                solution.append((r + rdiff, c))
                solution.append((r + rdiff, c + cdiff//2))
                solution.append((r + rdiff, c + cdiff))
                return True
            elif self.grid[r, c + cdiff//2] == 0 and self.grid[r + rdiff//2, c + cdiff] == 0:
                solution.append((r, c + cdiff//2))
                solution.append((r, c + cdiff))
                solution.append((r + rdiff//2, c + cdiff))
                solution.append((r + rdiff, c + cdiff))
                return True
            else:
                return False

        return False

    def _draw_guiding_line(self):
        """ draw a (mostly) straight line from start to end """
        r2, c2 = self.end
        path = []

        current = self.start
        if self._on_edge(self.start):
            current = self._push_edge(self.start)
        path.append(current)

        while not self._within_one(current, self.end):
            r1, c1 = current
            rdiff = cdiff = 0

            if abs(r1 - r2) > 1:
                rdiff = 2 if r1 < r2 else -2
            if abs(c1 - c2) > 1:
                cdiff = 2 if c1 < c2 else -2

            current = (r1 + rdiff, c1 + cdiff)
            path.append(current)

        return path

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

        # prune end point
        if solution[-1] == self.end:
            solution = solution[:-1]

        return solution
