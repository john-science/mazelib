
import unittest
from mazelib.generate.Prims import Prims
from mazelib.solve.WallFollower import WallFollower
from mazelib.mazelib import Maze


class SolversTest(unittest.TestCase):

    def within_one(self, cell1, cell2):
        """Is one cell within one move of another?"""
        r1,c1 = cell1
        r2,c2 = cell2

        if r1 == r2 and abs(c1 - c2) < 2:
            return True
        if c1 == c2 and abs(r1 - r2) < 2:
            return True

        return False

    def duplicates_in_solution(self, solution):
        """No cell should appear twice in the same maze solution."""
        for i in xrange(len(solution[:-1])):
            if solution[i] in solution[i+1:]:
                return True

        return False
    
    # TODO: Build test for one outer and one inner entrance

    def testWallFollower(self):
        m = Maze()
        m.generator = Prims(4, 5)
        m.generate()
        m.generate_entrances()
        m.solver = WallFollower()
        m.solve()

        for sol in m.solutions:
            self.assertFalse(self.duplicates_in_solution(sol))
            self.assertTrue(self.within_one(m.start, sol[0]))
            self.assertTrue(self.within_one(m.end, sol[-1]))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
