from random import choice
# If the code is not Cython-compiled, we need to add some imports.
from cython import compiled
if not compiled:
    from mazelib.solve.MazeSolveAlgo import MazeSolveAlgo


class Chain(MazeSolveAlgo):
    """
    1. draw a straight-ish line from start to end, ignore the walls.
    2. Follow the line from start to end.
        a. If you bump into a wall, you have to go around.
        b. Send out backtracking robots in the 1 or 2 open directions.
        c. If the robot can find your new point, continue on.
        d. If the robot intersects your line at a point that is further down stream,
            pick up the path there.
    3. repeat step 2 until you are at the end.
        a. If both robots return to their original location and direction,
            the maze is unsolvable.
    """

    def __init__(self, turn='right'):
        # turn can take on values 'left' or 'right'
        if turn == 'left':
            self.directions = [(-2, 0), (0, -2), (2, 0), (0, 2)]
        else:  # default to right turns
            self.directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]

    def _solve(self):
        """ solve a maze by trying to head directly, diagonally across the maze,
        when you hit a barrier, send out a back-tracking robot until you get to the next
        cell along the diagonal.

        Returns:
            list: maze solution path
        """
        guiding_line = self._draw_guiding_line()
        len_guiding_line = len(guiding_line)

        current = 0
        solution = [guiding_line[0]]

        while current < len_guiding_line - 1:
            # try to move to the next location
            success = self._try_direct_move(solution, guiding_line, current)
            if success:
                current += 1
            else:
                current = self._send_out_robots(solution, guiding_line, current)

        return [solution]

    def _send_out_robots(self, solution, guiding_line, i):
        """ send out backtracking robots in all directions, to look for the next point in the guiding line

        Args:
            solutions (list): The current solution path
            guiding_line (list): diagonal to the maze finish
            i (int): index of next step in maze
        Returns:
            int: position along the solution diagonal
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

        # randomly walk each robot, until it finds the guiding line or quits
        for j, path in enumerate(robot_paths):
            robot_paths[j] = self._backtracking_solve(path, guiding_line[i + 1])

        # add the shortest path to the solution
        shortest_robot_path = min(robot_paths, key=len)
        min_len = len(shortest_robot_path)
        for j, path in enumerate(robot_paths[1:]):
            if len(path) < min_len:
                shortest_robot_path = path
                min_len = len(path)
        solution += shortest_robot_path[1:]

        return guiding_line.index(solution[-1])

    def _backtracking_solve(self, solution, goal):
        """ our robots will attempt to solve the sub-maze using backtracking solver

        Args:
            solution (list): current path to the finish
            goal (tuple): next cell along the diagonal path to the finish
        Returns:
            list: new solution
        """
        path = list(solution)

        # pick a random neighbor and travel to it, until you're at the end
        while not self._within_one(path[-1], goal):
            ns = self._find_unblocked_neighbors(path[-1])

            # do no go where you've just been
            if len(ns) > 1 and len(path) > 2:
                if path[-3] in ns:
                    ns.remove(path[-3])

            nxt = choice(ns)
            path.append(self._midpoint(path[-1], nxt))
            path.append(nxt)

        return path

    def _try_direct_move(self, solution, guiding_line, i):
        """ The path to the next spot on the guiding line might be open.
        If so, add a couple steps to the solution. If not, return False.

        Args:
            solutions (list): The current solution path
            guiding_line (list): diagonal to the maze finish
            i (int): index of next step in maze
        Returns:
            bool: Did we find a better partial solution to the maze?
        """
        r, c = guiding_line[i]
        next = guiding_line[i + 1]

        rdiff = next[0] - r
        cdiff = next[1] - c

        # calculate the cell next door and see if it's open
        if rdiff == 0 or cdiff == 0:
            if self.grid[r + rdiff // 2, c + cdiff // 2] == 0:
                solution.append((r + rdiff // 2, c + cdiff // 2))
                solution.append((r + rdiff, c + cdiff))
                return True
        else:
            if self.grid[r + rdiff // 2, c] == 0 and self.grid[r + rdiff, c + cdiff // 2] == 0:
                solution.append((r + rdiff // 2, c))
                solution.append((r + rdiff, c))
                solution.append((r + rdiff, c + cdiff // 2))
                solution.append((r + rdiff, c + cdiff))
                return True
            elif self.grid[r, c + cdiff // 2] == 0 and self.grid[r + rdiff // 2, c + cdiff] == 0:
                solution.append((r, c + cdiff // 2))
                solution.append((r, c + cdiff))
                solution.append((r + rdiff // 2, c + cdiff))
                solution.append((r + rdiff, c + cdiff))
                return True
            else:
                return False

        return False

    def _draw_guiding_line(self):
        """ draw a (mostly) straight line from start to end

        Returns:
            list: the (probably digonal) straight line across the maze to the end
        """
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