
import unittest
from mazelib.generate.AldousBroder import AldousBroder
from mazelib.generate.BinaryTree import BinaryTree
from mazelib.generate.Prims import Prims
from mazelib.mazelib import Maze


class GeneratorsTest(unittest.TestCase):
    
    def boundary_is_solid(self, grid):
        """Algorithms should generate a maze with a solid boundary of walls."""
        # first row
        for c in grid[0]:
            if grid[r, c] == 0:
                return False

        # other rows
        for row in grid[1, -1]:
            if row[0] == 0 or row[-1] == 0:
                return False

        # last row
        for c in grid[-1]:
            if grid[r, c] == 0:
                return False

        return True

    def all_passages_open(self, grid):
        """All of the (odd, odd) grid cells in a maze should be passages."""
        H = grid.height
        W = grid.width

        for r in xrange(1, H, 2):
            for c in xrange(1, W, 2):
                if grid[r, c] == 1:
                    return False

        return True

    def all_corners_complete(self, grid):
        """All of the (even, even) grid cells in a maze should be walls."""
        H = grid.height
        W = grid.width

        for r in xrange(2, H, 2):
            for c in xrange(2, W, 2):
                if grid[r, c] == 0:
                    return False

        return True

    def testAldousBroder(self):
        m = Maze()
        m.generator = testAldousBroder(4, 5)
        m.generate()

        assertTrue(self.boundary_is_solid(m.grid))
        assertTrue(self.all_passages_open(m.grid))
        assertTrue(self.all_corners_complete(m.grid))

    def testBinaryTree(self):
        m = Maze()
        m.generator = BinaryTree(4, 5)
        m.generate()

        assertTrue(self.boundary_is_solid(m.grid))
        assertTrue(self.all_passages_open(m.grid))
        assertTrue(self.all_corners_complete(m.grid))

    def testPrims(self):
        m = Maze()
        m.generator = Prims(4, 5)
        m.generate()

        assertTrue(self.boundary_is_solid(m.grid))
        assertTrue(self.all_passages_open(m.grid))
        assertTrue(self.all_corners_complete(m.grid))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
