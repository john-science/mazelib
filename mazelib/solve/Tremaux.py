from random import choice
# If the code is not Cython-compiled, we need to add some imports.
from cython import compiled
if not compiled:
    from mazelib.solve.MazeSolveAlgo import MazeSolveAlgo


class Tremaux(MazeSolveAlgo):
    """ The Algorithm

    0. Every time you visit a cell, mark it once.
    1. When you hit a dead end, turn around and go back.
    2. When you hit a junction you haven't visited, pick a new passage at random.
    3. If you're walking down a new passage and hit a junction you have visited,
        treat it like a dead end and go back.
    4. If walking down a passage you have visited before (i.e. marked once) and you hit a junction,
        take any new passage available, otherwise take an old passage (i.e. marked once).
    5. When you finally reach the end, follow cells marked exactly once back to the start.
    6. If the Maze has no solution, you'll find yourself at the start with all cells marked twice.

    Results

    Finds one non-optimal solution.
    Works against imperfect mazes.

    Notes

    This Maze-solving method is designed to be used by a human inside the Maze.
    """
    def __init__(self):
        self.visited_cells = {}

    def _solve(self):
        """ implementing the algorithm

        Return:
            list: a single maze solution
        """
        self.visited_cells = {}
        solution = []

        # a first move has to be made
        current = self.start
        solution.append(current)
        self._visit(current)

        # if you're on the edge, push it in one
        if self._on_edge(self.start):
            current = self._push_edge(self.start)
            solution.append(current)
            self._visit(current)

        # pick a random neighbor using Tremaux logic and travel to it, until you're at the end
        while not self._within_one(solution[-1], self.end):
            # find the neighbors of the current cell
            ns = self._find_unblocked_neighbors(solution[-1])

            # pick the next cell based on the Tremaux logic
            nxt = self._what_next(ns, solution)

            # visit the new cell
            solution.append(self._midpoint(solution[-1], nxt))
            solution.append(nxt)
            self._visit(nxt)

        return [solution]

    def _visit(self, cell):
        """ Increment the number of times a cell has been visited.

        Args:
            cell (tuple): cell of interest
        Returns: None
        """
        if cell not in self.visited_cells:
            self.visited_cells[cell] = 0

        self.visited_cells[cell] += 1

    def _get_visit_count(self, cell):
        """ How many times has a cell been visited?

        Args:
            cell (tuple): cell of interest
        Returns:
            int: How many times has that cell been visited?
        """
        if cell not in self.visited_cells:
            return 0
        else:
            return self.visited_cells[cell] if self.visited_cells[cell] < 3 else 2

    def _what_next(self, ns, solution):
        """ Find the cell to move to next, based on the Tremaux logic:
        1. When you hit a dead end, turn around and go back.
        2. When you hit a junction you haven't visited, pick a new passage at random.
        3. If you're walking down a new passage and hit a junction you have visited,
            treat it like a dead end and go back.
        4. If walking down a passage you have visited before (i.e. marked once) and you hit a junction,
            take any new passage available, otherwise take an old passage (i.e. marked once).

        Args:
            ns (list): neighboring cells to choose next move from
            solution (list): the path we have taken so far
        Returns:
            tuple: the cell we want to move to next
        """
        # handle the easy scenario (and let this throw an error if ns is empty)
        if len(ns) <= 1:
            return ns[0]

        # organize the neighbors by their visit count
        visit_counts = {}
        for neighbor in ns:
            visit_count = self._get_visit_count(neighbor)
            if visit_count not in visit_counts:
                visit_counts[visit_count] = []
            visit_counts[visit_count].append(neighbor)

        # fullfill the Tremaux rules, using visit counts
        if 0 in visit_counts:
            # handle the case where we have no choice where to go
            return choice(visit_counts[0])
        elif 1 in visit_counts:
            # try not to backtrack, if you can
            if len(visit_counts[1]) > 1 and len(solution) > 2 and solution[-3] in visit_counts[1]:
                visit_counts[1].remove(solution[-3])
            return choice(visit_counts[1])
        else:
            # try not to backtrack, if you can
            if len(visit_counts[2]) > 1 and len(solution) > 2 and solution[-3] in visit_counts[2]:
                visit_counts[2].remove(solution[-3])
            return choice(visit_counts[2])