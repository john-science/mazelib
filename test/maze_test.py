
import numpy as np
import unittest
from mazelib.generate.Prims import Prims
from mazelib.solve.Collision import Collision
from mazelib.mazelib import Maze


class MazeTest(unittest.TestCase):
    
    def _on_edge(self, grid, cell):
        """ test helper method to determine if a point is on the edge of a maze
        """
        r, c = cell
        
        if r == 0 or r == (grid.shape[0] - 1):
            return True
        elif c == 0 or c == (grid.shape[1] - 1):
            return True
        
        return False

    def _num_turns(self, path):
        """ count the number of turns in a path """
        if len(path) < 3:
            return 0
    
        num = 0
    
        for i in range(1, len(path)-1):
            same_col = path[i-1][0] == path[i][0] == path[i+1][0]
            same_row = path[i-1][1] == path[i][1] == path[i+1][1]
            if not same_row and not same_col:
                num += 1
    
        return num

    def test_grid_size(self):
        h = 4
        w = 5
        H = 2 * h + 1
        W = 2 * w + 1

        m = Maze()
        m.generator = Prims(h, w)
        m.generate()

        self.assertEqual(m.grid.shape[0], H)
        self.assertEqual(m.grid.shape[1], W)

    def test_inner_entrances(self):
        h = 4
        w = 5

        m = Maze()
        m.generator = Prims(h, w)
        m.generate()
        m.generate_entrances(False, False)

        self.assertFalse(self._on_edge(m.grid, m.start))
        self.assertFalse(self._on_edge(m.grid, m.end))

    def test_outer_entrances(self):
        h = 4
        w = 5

        m = Maze()
        m.generator = Prims(h, w)
        m.generate()
        m.generate_entrances()

        self.assertTrue(self._on_edge(m.grid, m.start))
        self.assertTrue(self._on_edge(m.grid, m.end))

    def test_generator_wipe(self):
        h = 4
        w = 5

        m = Maze()
        m.generator = Prims(h, w)
        m.generate()
        m.generate_entrances()
        m.generate()

        self.assertTrue(m.start is None)
        self.assertTrue(m.end is None)
        self.assertTrue(m.solutions is None)

    def test_monte_carlo(self):
        h = 4
        w = 5
        H = 2 * h + 1
        W = 2 * w + 1

        m = Maze()
        m.generator = Prims(h, w)
        m.solver = Collision()
        m.generate_monte_carlo(3)

        # grid size
        self.assertEqual(m.grid.shape[0], H)
        self.assertEqual(m.grid.shape[1], W)

        # test entrances are outer
        self.assertTrue(self._on_edge(m.grid, m.start))
        self.assertTrue(self._on_edge(m.grid, m.end))

    def test_monte_carlo_reducer(self):
        h = 4
        w = 5
        H = 2 * h + 1
        W = 2 * w + 1

        m = Maze()
        m.generator = Prims(h, w)
        m.solver = Collision()
        m.generate_monte_carlo(3, reducer=self._num_turns)

        # grid size
        self.assertEqual(m.grid.shape[0], H)
        self.assertEqual(m.grid.shape[1], W)

        # test entrances are outer
        self.assertTrue(self._on_edge(m.grid, m.start))
        self.assertTrue(self._on_edge(m.grid, m.end))

    def test_maze_to_string(self):
        """ test that the 'to string' functionality is sane
        """
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

        s = str(m).split('\n')
        
        self.assertEqual(s[0].strip(), "#######")
        self.assertEqual(s[2].strip(), "# # ###")
        self.assertEqual(s[3].strip(), "# #   E")
        self.assertEqual(s[5].strip(), "S     #")
        self.assertEqual(s[6].strip(), "#######")

    def test_invalid_inputs(self):
        """ There are several errors that should be thrown from the master Maze class,
        if the inputs given are invalid.  Let's just verify some of those.
        """
        m = Maze()

        # should not be able to generate or solve if neither algorithm was set
        self.assertRaises(UnboundLocalError, m.generate)
        self.assertRaises(UnboundLocalError, m.solve)

        # even if the generator algorithm is set, you have to run it
        m.generator = Prims(3, 3)
        self.assertRaises(UnboundLocalError, m.solve)

        # the pretty-print, sring formats should fail gracefully
        m.start = (1, 1)
        m.end = (3, 3)
        self.assertEqual(str(m), '')
        self.assertEqual(repr(m), '')

        # the Monte Carlo method has a special zero-to-one input scalar
        self.assertRaises(ValueError, m.generate_monte_carlo, True, 3, -1.0)
        self.assertRaises(ValueError, m.generate_monte_carlo, True, 3, 10.0)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
