
from numpy.random import choice, shuffle
# If the code is not Cython-compiled, we need to add some imports.
try:
    from cython import compiled
except ModuleNotFoundError:
    compiled = False
if not compiled:
    from mazelib.solve.MazeSolveAlgo import MazeSolveAlgo

# CONSTANTS
END = (-999, -9)
DEAD_END = (-9, -999)


class Collision(MazeSolveAlgo):
    """
    1. step through the maze, flooding all directions equally
    2. if two flood paths meet, create a wall where they meet
    3. fill in all dead ends
    4. repeat until there are no more collisions
    """

    def _solve(self):
        # deal with the case where the start is on the edge
        start = self.start
        if self._on_edge(self.start):
            start = self._push_edge(self.start)

        # flood the maze twice, and compare the results
        paths = self._flood_maze(start)
        temp_paths = self._flood_maze(start)
        diff = list(set(map(tuple, paths)) - set(map(tuple, temp_paths)))

        # re-flood the maze until there are no more dead ends
        while diff:
            paths = temp_paths
            temp_paths = self._flood_maze(start)
            diff = list(set(map(tuple, paths)) - set(map(tuple, temp_paths)))

        paths = self._fix_entrances(paths)

        return paths

    def _flood_maze(self, start):
        """ from the start, flood the maze one cell at a time,
        keep track of where the water flows as paths through the maze
        """
        paths = self._one_time_step([[start]])
        temp_paths = paths

        while temp_paths is not None:
            paths = temp_paths
            temp_paths = self._one_time_step(paths)

        return paths

    def _one_time_step(self, paths):
        """ Move all open paths forward one grid cell """
        temp_paths = []
        step_made = False

        for path in paths:
            if path is None or path[-1] == DEAD_END:
                continue
            elif path[-1] == END:
                temp_paths.append(path)
                continue

            ns = self._find_unblocked_neighbors(path[-1])
            if len(path) > 2:
                if path[-3] in ns:
                    ns.remove(path[-3])

            if len(ns) == 0:
                temp_paths.append(path + [DEAD_END])
                step_made = True
            else:
                step_made = True
                for neighbor in ns:
                    mid = self._midpoint(path[-1], neighbor)
                    if self._within_one(neighbor, self.end):
                        temp_paths.append(path + [mid, neighbor, END])
                    else:
                        temp_paths.append(path + [mid, neighbor])

        if not step_made:
            return None

        # fix collisions
        temp_paths = self._fix_collisions(temp_paths)

        return temp_paths

    def _fix_collisions(self, paths):
        """look through paths for collsions
        If a collision exists, build a wall in the maze at that point."""
        N = len(paths)

        for i in range(N - 1):
            if paths[i][-1] in [DEAD_END, END]:
                continue
            for j in range(i + 1, N):
                if paths[j][-1] in [DEAD_END, END]:
                    continue
                if paths[i][-1] == paths[j][-1]:
                    row, col = paths[i][-1]
                    self.grid[row, col] = 1
                    paths[i][-1] = None
                    paths[j][-1] = None

        return paths

    def _fix_entrances(self, paths):
        """Ensure the start and end are appropriately placed in the solution."""
        # Filter out paths ending in 'dead_end'
        # (also: remove 'end' from solution paths)
        paths = [p[:-1] for p in paths if p[-1] != DEAD_END]

        # if start not on edge, remove first position in all paths
        if not self._on_edge(self.start):
            paths = [p[1:] for p in paths]

        # if end not on edge, remove last position in all paths
        if not self._on_edge(self.end):
            paths = [p[:-1] for p in paths]

        return paths
