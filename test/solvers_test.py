
import unittest
from mazelib.generate.Prims import Prims
from mazelib.solve.WallFollower import WallFollower
from mazelib.solve.ShortestPath import ShortestPath
from mazelib.solve.ShortestPaths import ShortestPaths
from mazelib.mazelib import Maze


class SolversTest(unittest.TestCase):

    def _within_one(self, cell1, cell2):
        """Is one cell within one move of another?"""
        r1,c1 = cell1
        r2,c2 = cell2

        if r1 == r2 and abs(c1 - c2) < 2:
            return True
        if c1 == c2 and abs(r1 - r2) < 2:
            return True

        return False

    def _duplicates_in_solution(self, solution):
        """No cell should appear twice in the same maze solution."""
        for i in xrange(len(solution[:-1])):
            if solution[i] in solution[i+1:]:
                return True

        return False

    def _create_maze_with_varied_entrances(self, start_outer=True, end_outer=True):
        """create a maze with entrances inside/outside"""
        m = Maze()
        m.generator = Prims(4, 5)
        m.generate()

        if start_outer and end_outer:
            m.generate_entrances()
        elif not start_outer and not end_outer:
            m.generate_entrances(False)
        else:
            if start_outer:
                m.start = (0, 3)
                m.end = (5, 5)
            else:
                m.start = (5, 5)
                m.end = (0, 3)

        return m

    def testWallFollower(self):
        """test against a maze with outer/inner entraces"""
        starts = [True, False]
        ends = [True, False]

        for s in starts:
            for e in ends:
                m = self._create_maze_with_varied_entrances(s, e)
                m.solver = WallFollower()
                m.solve()

                for sol in m.solutions:
                    self.assertFalse(self._duplicates_in_solution(sol))
                    self.assertTrue(self._within_one(m.start, sol[0]))
                    self.assertTrue(self._within_one(m.end, sol[-1]))

    def testShortestPath(self):
        """test against a maze with outer/inner entraces"""
        starts = [True, False]
        ends = [True, False]

        for s in starts:
            for e in ends:
                m = self._create_maze_with_varied_entrances(s, e)
                m.solver = ShortestPath()
                m.solve()

                for sol in m.solutions:
                    self.assertFalse(self._duplicates_in_solution(sol))
                    self.assertTrue(self._within_one(m.start, sol[0]))
                    self.assertTrue(self._within_one(m.end, sol[-1]))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
