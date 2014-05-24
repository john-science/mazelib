import copy
from random import choice,shuffle
from MazeSolveAlgo import MazeSolveAlgo


class DeadEndFiller(MazeSolveAlgo):
    """
    This is a simple Maze solving algorithm.
    It focuses on the Maze, is always very fast, and uses no extra
    memory.

    Just scan the Maze, and fill in each dead end, filling in the
    passage backwards from the block until you reach a junction. This
    includes filling in passages that become parts of dead ends once
    other dead ends are removed. At the end only the solution will
    remain, or solutions if there are more than one.

    This will always find the one unique solution for perfect Mazes,
    but won't do much in heavily braid Mazes, and in fact won't do
    anything useful at all for those Mazes without dead ends.
    """
    def __init__(self):


    def solve(self, grid, start, end):
        self.grid = copy.deepcopy(grid)
        self.grid[start] = self.grid[end] = 0
        current = start

        # loop through the maze serpentine, and find dead ends
        dead_end = self._find_dead_end(start, end)
        while dead_end != (-1, -1):
            # from the dead end, travel one cell.
            ns = self._find_neighbors(dead_end)

            # fill-in and wall-off the dead end
            self._fill_dead_end(dead_end)

            # look at the next cell, if it is a dead end, restart the loop
            if len(ns) == 1:
                # continue until you are in a junction cell.
                if self._is_dead_end(ns[0]):
                    dead_end = ns[0]
                    continue

            # otherwise, find another dead end in the maze
            dead_end = self._find_dead_end(start, end)

        # TODO
        # at this point, you have a grid with only solution tiles
        # however, you may have more than one solution, so you will have
        # to traverse the solution tiles and create multiple solutions
        solution = self._find_first_solution()
       
       
       
        return solution

    def _fill_dead_end(self, dead_end):

    def _fill_dead_end(self, dead_end):
        """After moving from a dead end, we want to fill in it and all
        the walls around it.
        """
        r,c = dead_end
        grid[r, c] = 1
        grid[r - 1, c] = 1
        grid[r + 1, c] = 1
        grid[r, c - 1] = 1
        grid[r, c + 1] = 1

    def _find_dead_end(self, start, end):
        """A "dead end" is a cell with only zero or one open neighbors.
        The start end end count as open.
        """
        for r in xrange(1, self.grid.height, 2):
            for c in xrange(1, self.grid.width, 2):
                if (n, c) in [start, end]:
                    continue
                if self._is_dead_end((r, c)):
                    return (r, c)

        return (-1, -1)

    def _is_dead_end(self, cell):
        """A dead end has zero or one open neighbors."""
        ns = self._find_neighbors(cell)
        if len(ns) in [0, 1]:
            return True
        else:
            return False

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

    def _midpoint(self, a, b):
        """Find the wall cell between to passage cells"""
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2
