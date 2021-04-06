import numpy as np
import unittest
from mazelib.mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.generate.TrivialMaze import TrivialMaze
from mazelib.transmute.CuldeSacFiller import CuldeSacFiller
from mazelib.transmute.DeadEndFiller import DeadEndFiller
from mazelib.transmute.Perturbation import Perturbation


class SolversTest(unittest.TestCase):

    def _example_cul_de_sac_maze(self):
        """ helper method to generate a super-simpl little maze with a loop in it:
        #######
              #
        # # # #
        # #   #
        # #####
        #
        #######
        """
        g = np.ones((7, 7), dtype=np.int8)
        g[1] = [1, 0, 0, 0, 0, 0, 1]
        g[2] = [1, 0, 1, 0, 1, 0, 1]
        g[3] = [1, 0, 1, 0, 0, 0, 1]
        g[4] = [1, 0, 1, 1, 1, 1, 1]
        g[5] = [1, 0, 0, 0, 0, 0, 1]

        return g

    def test_cul_de_sac_filler(self):
        """ Test the CuldeSacFiller leaves the maze in a solvable state """
        m = Maze()
        m.generator = Prims(3, 3)
        m.generate()
        m.grid = self._example_cul_de_sac_maze()

        assert m.grid[(1, 5)] == 0

        m.transmuters = [CuldeSacFiller()]
        m.transmute()

        assert m.grid[(1, 5)] == 1
        assert boundary_is_solid(m.grid)
        assert all_corners_complete(m.grid)

    def test_dead_end_filler(self):
        """ Test the CuldeSacFiller and DeadEndFiller leave the maze in a solvable state """
        m = Maze()
        m.generator = Prims(3, 3)
        m.generate()
        m.start = (1, 0)
        m.end = (5, 4)
        m.grid = self._example_cul_de_sac_maze()

        assert m.grid[(1, 5)] == 0
        assert m.grid[(1, 2)] == 0
        assert m.grid[(3, 3)] == 0

        m.transmuters = [CuldeSacFiller(), DeadEndFiller(99)]
        m.transmute()

        assert m.grid[(1, 5)] == 1
        assert m.grid[(1, 2)] == 1
        assert m.grid[(3, 3)] == 1

        assert boundary_is_solid(m.grid)
        assert all_corners_complete(m.grid)

    def test_perturbation(self):
        """ Test the Perturbation algorithm leaves the maze in a solvable state """
        m = Maze()
        m.generator = TrivialMaze(4, 5)
        m.generate()

        m.transmuters = [Perturbation()]
        m.transmute()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)


def boundary_is_solid(grid):
    """ Helper method to test of the maze is sane
    Algorithms should generate a maze with a solid boundary of walls.

    Args:
        grid (np.array): maze array
    Returns:
        boolean: is the maze boundary solid?
    """
    # first row
    for c in grid[0]:
        if c == 0:
            return False

    # other rows
    for row in grid[1: -1]:
        if row[0] == 0 or row[-1] == 0:
            return False

    # last row
    for c in grid[grid.shape[0] - 1]:
        if c == 0:
            return False

    return True


def all_passages_open(grid):
    """ Helper method to test of the maze is sane
    All of the (odd, odd) grid cells in a maze should be passages.

    Args:
        grid (np.array): maze array
    Returns:
        booean: Are all the odd/odd grid cells open?
    """
    H, W = grid.shape

    for r in range(1, H, 2):
        for c in range(1, W, 2):
            if grid[r, c] == 1:
                return False

    return True


def all_corners_complete(grid):
    """ Helper method to test of the maze is sane
    All of the (even, even) grid cells in a maze should be walls.

    Args:
        grid (np.array): maze array
    Returns:
        boolean: Are all of the grid corners solid?
    """
    H, W = grid.shape

    for r in range(2, H, 2):
        for c in range(2, W, 2):
            if grid[r, c] == 0:
                return False

    return True


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
