
from array import array
import unittest
from mazelib.utils.array2d import Array2D
from mazelib.utils.MazeArray import MazeArray


class ArrayTest(unittest.TestCase):

    def testDefault(self):
        a = Array2D('b', (5, 5), True)
        self.assertTrue(a[0, 0])
        self.assertTrue(a[1, 1])

    def testSize(self):
        a = Array2D('b', (5, 5), True)
        self.assertEqual(a.height, 5)
        self.assertEqual(a.width, 5)
        self.assertEqual(len(a), 25)

    def testGetAndSetElement(self):
        a = Array2D('b', (5, 5), True)
        self.assertTrue(a[1,2])
        a[1,2] = 0
        self.assertFalse(a[1,2])

    def testGetAndSetTuple(self):
        a = Array2D('b', (5, 5), True)
        self.assertTrue(a[(1,2)])
        a[(1,2)] = 0
        self.assertFalse(a[(1,2)])

    def testGetAndSetRow(self):
        # create 2d array, defaulted to all True
        dim = 5
        a = Array2D('b', (dim, dim), True)
        # test that all values are true
        for col in a[0]:
            self.assertTrue(col)
        # set the first row to an all-false array
        row = array('b', [0] *dim)
        a[0] = row
        # test that the first row was changed correctly
        for col in a[0]:
            self.assertFalse(col)

    def testGetSlice(self):
        # create 2d array, defaulted to all True
        dim = 5
        a = Array2D('b', (dim, dim), True)

        # get first two rows, by slice
        a_slice = a[:2]
        self.assertEquals(a_slice.height, 2)
        for row in a_slice:
            for col in row:
                self.assertTrue(col)

    def testMazeArrayDefault(self):
        m = MazeArray(5, 5)
        self.assertTrue(m[0, 0])
        self.assertTrue(m[1, 1])

    def testMazeArraySize(self):
        m = MazeArray(5, 5)
        self.assertEqual(m.height, 5)
        self.assertEqual(m.width, 5)
        self.assertEqual(len(m), 25)

    def testMazeArrayGetAndSetElement(self):
        m = MazeArray(5, 5)
        self.assertTrue(m[1,2])
        m[1,2] = 0
        self.assertFalse(m[1,2])


def main():
    unittest.main()


if __name__ == '__main__':
    main()
