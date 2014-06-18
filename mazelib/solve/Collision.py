from random import choice,shuffle
from MazeSolveAlgo import MazeSolveAlgo


class Collision(MazeSolveAlgo):
    """
    1) step through the maze, flooding all directions equally
    2) if two flood paths meet, create a wall where they meet
    3) fill in all dead ends
    4) repeat until there are no more collisions
    """
    def _solve(self):
        # deal with the case where the start is on the edge
        start = self.start
        if self._on_edge(self.start):
            start = self._push_edge_start(self.start)

        # flood the maze twice, and compare the results
        paths = self._flood_maze(start)
        temp_paths = self._flood_maze(start)
        diff = list(set(map(tuple, paths)) - set(map(tuple, temp_paths)))

        # re-flood the maze until there are no more dead ends
        while diff:
            paths = temp_paths
            temp_paths = self._flood_maze(start)
            diff = list(set(map(tuple, paths)) - set(map(tuple, temp_paths)))

        # Filter out paths ending in 'dead_end'
        paths = filter(lambda p: p[-1] != 'dead_end', paths)
        # remove 'end' from solution paths
        paths = map(lambda p: p[:-1], paths)
        # if start not on edge, remove first position in all paths
        if not self._on_edge(self.start):
            paths = map(lambda p: p[1:], paths)
        # if end not on edge, remove last position in all paths
        if not self._on_edge(self.end):
            paths = map(lambda p: p[:-1], paths)

        return paths

    def _flood_maze(self, start):
        """from the start, flood the maze one cell at a time,
        keep track of where the water flows as paths through the maze
        """
        paths = self._one_time_step([[start]])
        temp_paths = paths

        while temp_paths is not None:
            paths = temp_paths
            temp_paths = self._one_time_step(paths)

        return paths

    def _one_time_step(self, paths):
        """Move all open paths forward one grid cell"""
        temp_paths = []
        step_made = False

        for path in paths:
            if path is None or path[-1] == 'dead_end':
                continue
            elif path[-1] == 'end':
                temp_paths.append(path)
                continue

            ns = self._find_unblocked_neighbors(path[-1])
            if len(path) > 2:
                ns.remove(path[-3])

            if len(ns) == 0:
                temp_paths.append(path + ['dead_end'])
                step_made = True
            else:
                step_made = True
                for neighbor in ns:
                    mid = self._midpoint(path[-1], neighbor)
                    if self._within_one(neighbor, self.end):
                        temp_paths.append(path + [mid, neighbor, 'end'])
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

        for i in xrange(N - 1):
            if paths[i][-1] in ['dead_end', 'end']:
                continue
            for j in xrange(i + 1, N):
                if paths[j][-1] in ['dead_end', 'end']:
                    continue
                if paths[i][-1] == paths[j][-1]:
                    self.grid[paths[i][-1]] = 1
                    paths[i][-1] = None
                    paths[j][-1] = None

        return paths

    def _within_one(self, cell, desire):
        """Is the current cell within one move of the desired cell?
        Note, this might be one full more, or one half move.
        """
        if not cell or not desire:
            return False

        rdiff = abs(cell[0] - desire[0])
        cdiff = abs(cell[1] - desire[1])

        if rdiff == 0 and cdiff < 2:
            return True
        elif cdiff == 0 and rdiff < 2:
            return True

        return False

    def _on_edge(self, cell):
        """Does the cell lay on the edge, rather inside of the maze grid?"""
        r,c = cell

        if r == 0 or r == self.grid.height - 1:
            return True
        if c == 0 or c == self.grid.width - 1:
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

    def _find_unblocked_neighbors(self, posi):
        """Find all the grid neighbors of the current position;
        visited, or not.
        """
        (row, col) = posi
        ns = []

        if row > 1 and self.grid[row-1, col] == False and self.grid[row-2, col] == False:
            ns.append((row-2, col))
        if row < self.grid.height-2 and self.grid[row+1, col] == False and self.grid[row+2, col] == False:
            ns.append((row+2, col))
        if col > 1 and self.grid[row, col-1] == False and self.grid[row, col-2] == False:
            ns.append((row, col-2))
        if col < self.grid.width-2 and self.grid[row, col+1] == False and self.grid[row, col+2] == False:
            ns.append((row, col+2))

        shuffle(ns)

        return ns

    def _midpoint(self, a, b):
        """Find the wall cell between to passage cells"""
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2
