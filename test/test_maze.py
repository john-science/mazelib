import numpy as np
import unittest
from mazelib.generate.Prims import Prims
from mazelib.solve.Collision import Collision
from mazelib.mazelib import Maze


class MazeTest(unittest.TestCase):

    def _on_edge(self, grid, cell):
        """ helper method to determine if a point is on the edge of a maze

        Args:
            grid (np.array): maze array
            cell (tuple): position of cell of interest
        Returns:
            boolean: Is this cell on the edge of the maze?
        """
        r, c = cell

        if r == 0 or r == (grid.shape[0] - 1):
            return True
        elif c == 0 or c == (grid.shape[1] - 1):
            return True

        return False

    def _num_turns(self, path):
        """ helper method to count the number of turns in a path

        Args:
            path (list): sequence of cells to path through maze
        Returns:
            int: number of turns in the path
        """
        if len(path) < 3:
            return 0

        num = 0
        for i in range(1, len(path) - 1):
            same_col = path[i - 1][0] == path[i][0] == path[i + 1][0]
            same_row = path[i - 1][1] == path[i][1] == path[i + 1][1]
            if not same_row and not same_col:
                num += 1

        return num

    def test_grid_size(self):
        """ Test that the array representation for the maze is the exact size we want it to be """
        h = 4
        w = 5
        H = 2 * h + 1
        W = 2 * w + 1

        m = Maze()
        m.generator = Prims(h, w)
        m.generate()

        assert m.grid.shape[0] == H
        assert m.grid.shape[1] == W

    def test_inner_entrances(self):
        """ Test that the entrances can be correctly generated not on the edges of the map """
        h = 4
        w = 5

        m = Maze()
        m.generator = Prims(h, w)
        m.generate()
        m.generate_entrances(False, False)

        assert not self._on_edge(m.grid, m.start)
        assert not self._on_edge(m.grid, m.end)

    def test_outer_entrances(self):
        """ Test that the entrances can be correctly generated on the edges of the map """
        h = 4
        w = 5

        m = Maze()
        m.generator = Prims(h, w)
        m.generate()
        m.generate_entrances()

        assert self._on_edge(m.grid, m.start)
        assert self._on_edge(m.grid, m.end)

    def test_generator_wipe(self):
        """ Test that the running the master generate() method twice correctly wipes the entrances and solutions """
        h = 4
        w = 5

        m = Maze()
        m.generator = Prims(h, w)
        m.generate()
        m.generate_entrances()
        m.generate()

        assert m.start is None
        assert m.end is None
        assert m.solutions is None

    def test_monte_carlo(self):
        """ Test that the basic Monte Carlo maze generator """
        h = 4
        w = 5
        H = 2 * h + 1
        W = 2 * w + 1

        m = Maze()
        m.generator = Prims(h, w)
        m.solver = Collision()
        m.generate_monte_carlo(3)

        # grid size
        assert m.grid.shape[0] == H
        assert m.grid.shape[1] == W

        # test entrances are outer
        assert self._on_edge(m.grid, m.start)
        assert self._on_edge(m.grid, m.end)

    def test_monte_carlo_reducer(self):
        """ Test that the reducer functionality on the Monte Carlo maze generator """
        h = 4
        w = 5
        H = 2 * h + 1
        W = 2 * w + 1

        m = Maze()
        m.generator = Prims(h, w)
        m.solver = Collision()
        m.generate_monte_carlo(3, reducer=self._num_turns)

        # grid size
        assert m.grid.shape[0] == H
        assert m.grid.shape[1] == W

        # test entrances are outer
        assert self._on_edge(m.grid, m.start)
        assert self._on_edge(m.grid, m.end)

    def test_maze_to_string(self):
        """ Test that the 'to string' functionality is sane """
        m = Maze()
        m.generator = Prims(3, 3)

        # fake some maze results, to test against
        m.grid = np.array([[1, 1, 1, 1, 1, 1, 1],
                           [1, 0, 0, 0, 0, 0, 1],
                           [1, 0, 1, 0, 1, 1, 1],
                           [1, 0, 1, 0, 0, 0, 1],
                           [1, 1, 1, 0, 1, 1, 1],
                           [1, 0, 0, 0, 0, 0, 1],
                           [1, 1, 1, 1, 1, 1, 1]])
        m.start = (5, 0)
        m.end = (3, 6)
        m.solutions = [[(5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (4, 5), (3, 5)]]

        s = str(m).split('\n')

        assert s[0].strip() == "#######"
        assert s[2].strip() == "# # ###"
        assert s[3].strip() == "# #  +E"
        assert s[5].strip() == "S+++++#"
        assert s[6].strip() == "#######"

    def test_invalid_inputs(self):
        """ Test that the correct errors are thrown when the top-level methods are called incorrectly """
        m = Maze()

        # should not be able to generate or solve if neither algorithm was set
        self.assertRaises(AssertionError, m.generate)
        self.assertRaises(AssertionError, m.solve)

        # even if the generator algorithm is set, you have to run it
        m.generator = Prims(3, 3)
        self.assertRaises(AssertionError, m.solve)

        # the pretty-print, sring formats should fail gracefully
        m.start = (1, 1)
        m.end = (3, 3)
        assert str(m) == ''
        assert repr(m) == ''

        # the Monte Carlo method has a special zero-to-one input scalar
        self.assertRaises(AssertionError, m.generate_monte_carlo, True, 3, -1.0)
        self.assertRaises(AssertionError, m.generate_monte_carlo, True, 3, 10.0)

    def test_set_seed(self):
        """ Test the Maze.set_seed staticmethod, to make sure we can control the random seeding """
        m = Maze(123)
        m.generator = Prims(7, 7)
        m.generate()
        grid0 = str(m)

        m = Maze(123)
        m.generator = Prims(7, 7)
        m.generate()
        grid1 = str(m)

        assert grid0 == grid1

        m.generator = Prims(7, 7)
        m.generate()
        grid2 = str(m)

        assert grid0 != grid2


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
