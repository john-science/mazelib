
from random import choice,shuffle
from MazeSolveAlgo import MazeSolveAlgo
from ShortestPaths import ShortestPaths


class CuldeSacFiller(MazeSolveAlgo):
    """
    1. Scan the maze, identify all fully-connected wall systems.
    2. Any wall system that touches the border is not a cul-de-sac, remove it.
    3. Determine if remaining wall systems are cul-de-sacs.
    4. If so, add a wall segment to turn the cul-de-sac into a dead end.
    5. Solve using Dead End Filler.
    """
    def __init__(self, solver=None):
        if not solver:
            self.solver = DeadEndFiller(ShortestPaths())
        else:
            self.solver = DeadEndFiller(solver)

    def _solve(self):
        raise NotImplementedError('This algorithm is under development.')
        current = self.start

        # identify all fully-connected wall systems
        walls = self._find_wall_systems()

        # remove any wall system that touches the maze boundary
        walls = self._remove_border_walls(walls)

        for wall in walls:
            if self._is_culdesac(wall):
                self._fix_culdesac(wall)

        return self._build_solutions()

    def _build_solutions(self):
        """Now that all of the cul-de-sac have been cut out, the maze still needs to be solved."""
        return self.solver.solve(self.grid, self.start, self.end)

    def _is_culdesac(self, cell):
        """A cul-de-sac is a loop with only one entrance."""
        exit('Not implemented')

    def _fix_culdesac(self, cell):
        """Destroy the culdesac by blocking off the loop."""
        exit('Not implemented')

    def _remove_border_walls(self, walls):
        """remove any wall system that touches the maze border"""
        new_walls = []

        for wall in walls:
            touches_border = False
            for cell in wall:
                if self._is_on_border(cell):
                    touches_border = True
                    break
            if not touches_border:
                new_walls.append(wall)

        return new_walls

    def _is_on_border(self, cell):
        """Determine is a cell is on the border of the maze"""
        r,c = cell

        if r == 0 or c == 0:
            return True
        elif r == (self.grid.height - 1):
            return True
        elif c == (self.grid.width - 1):
            return True
        else:
            return False

    def _find_wall_systems(self):
        """A wall system is any continiously-adjacent set of walls."""
        walls = []
        # loop through each cell in the maze
        for r in xrange(self.grid.height):
            for c in xrange(self.grid.width):
                # if the cell is a wall
                if self.grid[r, c] == 1:
                    found = False
                    # determine which wall system it belongs in
                    for i in xrange(len(walls)):
                        if self._has_neighbor((r, c), walls[i]):
                            found = True
                            walls[i].append((r, c))
                    if not found:
                        walls.append([(r, c)])

        return walls

    def _is_neighbor(self, cell1, cell2):
        """Determine if one cell is adjacent to another"""
        r_diff = abs(cell1[0] - cell2[0])
        c_diff = abs(cell1[1] - cell2[1])

        if r_diff == 0 and c_diff == 1:
            return True
        elif c_diff == 0 and r_diff == 1:
            return True
        else:
            return False

    def _has_neighbor(self, cell, list_cells):
        """Determine if your cell has a neighbor in a list of cells"""
        for target in list_cells:
            if self._is_neighbor(cell, target):
                return True

        return False

    def _is_culdesac(self, cell):
        """A cul-de-sac is a loop with only one entrance."""
        exit('Not implemented')

    def _find_unblocked_neighbors(self, posi, visited=True):
        """Find all the grid neighbors of the current position;
        visited, or not.
        """
        (row, col) = posi
        ns = []

        if row > 1 and self.grid[row-1, col] != visited and self.grid[row-2, col] != visited:
            ns.append((row-2, col))
        if row < self.grid.height-2 and self.grid[row+1, col] and self.grid[row+2, col] != visited:
            ns.append((row+2, col))
        if col > 1 and self.grid[row, col-1] and self.grid[row, col-2] !d= visited:
            ns.append((row, col-2))
        if col < self.grid.width-2 and self.grid[row, col+1] and self.grid[row, col+2] != visited:

            ns.append((row, col+2))

        shuffle(ns)

        return ns

    def _find_neighbors(self, posi, visited=True):
        """Find all the grid neighbors of the current position;
        visited, or not.
        """
        (row, col) = posi
        ns = []

        if row > 1 and self.grid[row-2, col] != visited:
            ns.append((row-2, col))
        if row < self.grid.height-2 and self.grid[row+2, col] != visited:
            ns.append((row+2, col))
        if col > 1 and self.grid[row, col-2] != visited:
            ns.append((row, col-2))
        if col < self.grid.width-2 and self.grid[row, col+2] != visited:

            ns.append((row, col+2))

        shuffle(ns)

        return ns
