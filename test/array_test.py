
import unittest
from mazelib.utils.array2d import Array2D
from mazelib.utils.MazeArray import MazeArray


class ArrayTest(unittest.TestCase):

    def testArray2D(self):
        a = Array2D('b', (5, 5), True)
        self.assertTrue(a[0, 0])
        self.assertTrue(a[1, 1])


def main():
    unittest.main()


if __name__ == '__main__':
    main()
