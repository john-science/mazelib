
import unittest
from mazelib.generate.Prims import Prims
from mazelib.solve.Collision import Collision
from mazelib.mazelib import Maze


class MazeTest(unittest.TestCase):
    
    def _on_edge(self, grid, cell):
        """ test helper method to determine if a point
            is on the edge of a maze
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

    def testGridSize(self):
        h = 4
        w = 5
        H = 2 * h + 1
        W = 2 * w + 1

        m = Maze()
        m.generator = Prims(h, w)
        m.generate()

        self.assertEqual(m.grid.shape[0], H)
        self.assertEqual(m.grid.shape[1], W)

    def testInnerEntrances(self):
        h = 4
        w = 5

        m = Maze()
        m.generator = Prims(h, w)
        m.generate()
        m.generate_entrances(False, False)

        self.assertFalse(self._on_edge(m.grid, m.start))
        self.assertFalse(self._on_edge(m.grid, m.end))

    def testOuterEntrances(self):
        h = 4
        w = 5

        m = Maze()
        m.generator = Prims(h, w)
        m.generate()
        m.generate_entrances()

        self.assertTrue(self._on_edge(m.grid, m.start))
        self.assertTrue(self._on_edge(m.grid, m.end))

    def testGeneratorWipe(self):
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

    def testMonteCarlo(self):
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

    def testMonteCarloReducer(self):
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


def main():
    unittest.main()


if __name__ == '__main__':
    main()
