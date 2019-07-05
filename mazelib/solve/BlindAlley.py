
from random import choice,shuffle
# If the code is not Cython-compiled, we need to add some imports.
try:
    from cython import compiled
except ModuleNotFoundError:
    compiled = False
if not compiled:
    from mazelib.solve.MazeSolveAlgo import MazeSolveAlgo
    from mazelib.solve.ShortestPaths import ShortestPaths

FILLER = 1
SEALER = 2


class BlindAlley(MazeSolveAlgo):
    """
    1. Scan the maze, identify all fully-connected wall systems.
    2. Any wall system that touches the border is not a cul-de-sac, remove it.
    3. Determine if remaining wall systems are cul-de-sacs.
    4. If so, add a wall segment to turn the cul-de-sac into a dead end.
    5. Solve using Dead End Filler.
    """
    def __init__(self, fill_type='filler', solver=None):
        if not solver:
            self.solver = ShortestPaths()
        else:
            self.solver = solver

        if fill_type == 'sealer':
            self._remove_dead_end = SEALER
        else:
            self._remove_dead_end = FILLER

    def _solve(self):
        # TODO: There is a wall detection problem here. Seal cul-de-sacs fails on rare occassion.
        #self._seal_culdesacs()
        self._fill_dead_ends()

        return self._build_solutions()

    def _seal_culdesacs(self):
        """ identify and seal off all culdesacs """
        # identify all fully-connected wall systems
        walls = self._find_wall_systems()
        # connect wall systems that are disconnected above
        walls = self._reduce_wall_systems(walls)

        # remove any wall system that touches the maze boundary
        walls = self._remove_border_walls(walls)

        for wall in walls:
            border = self._find_bordering_cells(wall)
            if self._wall_is_culdesac(border):
                self._fix_culdesac(border)

    def _reduce_wall_systems(self, walls):
        """ Reduce a collection of walls in a maze to realize
        when two walls are actually connected and should be one.
        """
        N = len(walls)

        for i in range(N - 1):
            if walls[i] is None:
                continue
            for j in range(i, N):
                if walls[j] is None:
                    continue
                if self._walls_are_connected(walls[i], walls[j]):
                    walls[i] += walls[j]
                    walls[j] = None

        # remove "None" walls
        return [w for w in walls if w != None]

    def _walls_are_connected(self, wall1, wall2):
        """ Figure out if two walls are connected at any point. """
        if wall1 is None or wall2 is None:
            return False

        for cell1 in wall1:
            for cell2 in wall2:
                if self._is_neighbor(cell1, cell2):
                    return True

        return False

    def _build_solutions(self):
        """ Now that all of the cul-de-sac have been cut out,
        the maze still needs to be solved.
        """
        return self.solver.solve(self.grid, self.start, self.end)

    def _fix_culdesac(self, border):
        """ Destroy the culdesac by blocking off the loop. """
        if len(border) > 1:
            r, c = self._midpoint(border[0], border[1])
            self.grid[r, c] = 1

    def _wall_is_culdesac(self, border):
        """ A cul-de-sac is a loop with only one entrance. """
        num_entrances = 0

        for cell in border:
            num_neighbors = len(self._find_unblocked_neighbors(cell))
            # if a cell has more than 2 neighbors, one must be a cul-de-sac entrance
            if num_neighbors > 2:
                num_entrances += 1
            # if it has more than one entrance, it's not a cul-de-sac
            if num_entrances > 1:
                return False

        return True

    def _find_bordering_cells(self, wall):
        """ build a buffer, one cell wide, around the wall """
        border = []

        # buffer each wall cell by one, append those buffer cells to a list
        for cell in wall:
            r, c = cell
            for rdiff in range(-1, 2):
                for cdiff in range(-1, 2):
                    border.append((r + rdiff, c + cdiff))

        # remove all non-unique cells
        border = list(set(border))

        # remove all wall cells from the buffer
        border = [b for b in border if b not in wall]

        # remove all non-navigable cells from the buffer
        border = [b for b in border if b[0] % 2 == 1 and b[1] % 2 == 1]

        # remove all dead ends within the cul-de-sac
        return self._remove_internal_deadends(border)

    def _remove_internal_deadends(self, border):
        """ Complicated cul-de-Sacs can have internal dead ends.
        These seriously complicate the logic and need to be removed.
        """
        found = True
        while found:
            found = False
            new_border = border
            for cell in border:
                if len(self._find_unblocked_neighbors(cell)) < 2:
                    new_border.remove(cell)
                    found = True
            border = new_border

        return border

    def _remove_border_walls(self, walls):
        """ remove any wall system that touches the maze border """
        new_walls = []

        for wall in walls:
            on_edge = False
            for cell in wall:
                if self._on_edge(cell):
                    on_edge = True
                    break
            if not on_edge:
                new_walls.append(wall)

        return new_walls

    def _find_wall_systems(self):
        """ A wall system is any continiously-adjacent set of walls. """
        walls = []
        # loop through each cell in the maze
        for r in range(self.grid.shape[0]):
            for c in range(self.grid.shape[1]):
                # if the cell is a wall
                if self.grid[r, c] == 1 and (r, c) not in (self.start, self.end):
                    found = False
                    # determine which wall system it belongs in
                    for i in range(len(walls)):
                        if self._has_neighbor((r, c), walls[i]):
                            found = True
                            walls[i].append((r, c))
                    if not found:
                        walls.append([(r, c)])

        return walls

    def _is_neighbor(self, cell1, cell2):
        """ Determine if one cell is adjacent to another """
        r_diff = abs(cell1[0] - cell2[0])
        c_diff = abs(cell1[1] - cell2[1])

        if r_diff == 0 and c_diff == 1:
            return True
        elif c_diff == 0 and r_diff == 1:
            return True
        else:
            return False

    def _has_neighbor(self, cell, list_cells):
        """ Determine if your cell has a neighbor in a list of cells """
        for target in list_cells:
            if self._is_neighbor(cell, target):
                return True

        return False

    def _fill_dead_ends(self):
        """ fill all dead ends in the maze """
        # loop through the maze serpentine, and find dead ends
        for r in range(1, self.grid.shape[0], 2):
            for c in range(1, self.grid.shape[1], 2):
                if self._is_dead_end((r, c)):
                    # fill-in or wall-off the dead end
                    if self._remove_dead_end == SEALER:
                        self._dead_end_sealer((r, c))
                    else:
                        self._dead_end_filler((r, c))

    def _dead_end_filler(self, dead_end):
        """ Back away from the dead end until you reach an intersection.
        Fill the path as you go.
        """
        r, c = dead_end
        ns = self._find_unblocked_neighbors((r, c))

        if len(ns) == 1:
            self.grid[r, c] = 1
            r, c = self._midpoint(ns[0], (r, c))
            self.grid[r, c] = 1

    def _dead_end_sealer(self, dead_end):
        """ Back away from the dead end until you reach an intersection.
        Block off the dead end passage.
        """
        current = dead_end
        ns = self._find_unblocked_neighbors(current)

        if len(ns) == 1:
            last = current
            current = ns[0]

            r, c = self._midpoint(last, current)
            self.grid[r, c] = 1

    def _is_dead_end(self, cell):
        """ A dead end has zero or one open neighbors. """
        ns = self._find_unblocked_neighbors(cell)

        if self._within_one(cell, self.start) or self._within_one(cell, self.end):
            return False
        elif self.grid[cell[0], cell[1]] == True:  # TODO: WARNING: Index should be typed for more efficient access
            return False
        elif len(ns) in [0, 1]:
            return True
        else:
            return False
