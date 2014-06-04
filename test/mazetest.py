
import unittest
from mazelib.generate.Prims import Prims
from mazelib.mazelib import Maze


class MazeTest(unittest.TestCase):

    def testGridSize(self):
        h = 10
        w = 21
        H = 2 * h + 1
        W = 2 * w + 1

        m = Maze()
        m.generator = Prims(h, w)
        m.generate()

        self.assertEqual(m.grid.height, H)
        self.assertEqual(m.grid.width, W)
   
    """
    TODO: Tests to Build
   
    test that inner/outer entrance generators work
    test that running a generator wipes the entrances and solutions clear
    test that Monte Carlo doesn't explode?
    test tostring method
    """


def main():
    unittest.main()


if __name__ == '__main__':
    main()
