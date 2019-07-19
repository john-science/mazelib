
import numpy as np
import unittest
from mazelib.generate.Prims import Prims
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
from mazelib.solve.Chain import Chain
from mazelib.solve.Collision import Collision
from mazelib.solve.RandomMouse import RandomMouse
from mazelib.solve.ShortestPath import ShortestPath
from mazelib.solve.ShortestPaths import ShortestPaths
from mazelib.mazelib import Maze


class SolversTest(unittest.TestCase):

    def _one_away(self, cell1, cell2):
        """ Is one cell exactly one move from another? """
        r1,c1 = cell1
        r2,c2 = cell2

        if r1 == r2 and abs(c1 - c2) == 1:
            return True
        elif c1 == c2 and abs(r1 - r2) == 1:
            return True

        return False

    def _duplicates_in_solution(self, solution):
        """ No cell should appear twice in the same maze solution. """
        for i in range(len(solution[:-1])):
            if solution[i] in solution[i+1:]:
                return True

        return False

    def _create_maze_with_varied_entrances(self, start_outer=True, end_outer=True):
        """ create a maze with entrances inside/outside """
        m = Maze()
        m.generator = Prims(4, 5)
        m.generate()

        if start_outer and end_outer:
            m.generate_entrances()
        elif not start_outer and not end_outer:
            m.generate_entrances(False, False)
        elif start_outer:
             m.generate_entrances(True, False)
        else:
             m.generate_entrances(False, True)

        return m

    def test_prune_solution(self):
        """ test the solution-pruning helper method """
        # build a test Maze and solver, just as placeholders
        m = Maze()
        m.solver = RandomMouse()
        m.solver.start = (0, 1)
        m.solver.end = (0, 5)

        # test the pruner does nothing if nothing needs to be done
        sol = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
        assert sol == m.solver._prune_solution(sol)

        # test the pruner correctly prunes one duplicate
        sol1 = [(1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (2, 4), (1, 4), (1, 5)]
        assert sol == m.solver._prune_solution(sol1)

        # test the pruner correctly prunes two duplicates
        sol2 = [(1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (2, 4), (1, 4), (2, 4), (3, 4),
                (2, 4), (1, 4), (1, 5)]
        assert sol == m.solver._prune_solution(sol2)

        # test the pruner correctly prunes the end point from the solution
        sol3 = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (0, 5)]
        assert sol == m.solver._prune_solution(sol3)

        # test the pruner correctly prunes the start point from the solution
        sol4 = [(0, 1), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
        assert sol == m.solver._prune_solution(sol4)

        # test the pruner correctly prunes the start points and end points from the solution
        sol5 = [(0, 1), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (0, 5)]
        assert sol == m.solver._prune_solution(sol5)

        # test the pruner correctly prunes multiple start points and end points from the solution
        sol6 = [(0, 1), (0, 1), (0, 1), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (0, 5), (0, 5)]
        assert sol == m.solver._prune_solution(sol6)

        # test the pruner correctly prunes a complex mess of a solution
        sol7 = [(0, 1), (0, 1), (0, 1), (1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (2, 4),
                (1, 4), (1, 5), (0, 5), (0, 5)]
        assert sol == m.solver._prune_solution(sol7)
        # bonus: let's tests a long, and heavily redundant, solution
        assert sol == m.solver._prune_solution(sol7*100)

        # let's also test a couple edge cases
        sol = []
        assert sol == m.solver._prune_solution(sol)
        sol = [(1, 1)]
        assert sol == m.solver._prune_solution(sol)
        sol = [(1, 1), (1, 2)]
        assert sol == m.solver._prune_solution(sol)
        sol = [(1, 1), (1, 2)]
        assert sol == m.solver._prune_solution(sol*100)

    def test_backtracking_solver(self):
        """ test BacktrackingSolver against a maze with outer/inner entraces """
        starts = [True, False]
        ends = [True, False]

        for s in starts:
            for e in ends:
                m = self._create_maze_with_varied_entrances(s, e)
                m.solver = BacktrackingSolver()
                m.solve()

                for sol in m.solutions:
                    self.assertFalse(self._duplicates_in_solution(sol))
                    self.assertTrue(self._one_away(m.start, sol[0]))
                    self.assertTrue(self._one_away(m.end, sol[-1]))

    def test_chain(self):
        """ test against a maze with outer/inner entraces """
        starts = [True, False]
        ends = [True, False]

        for s in starts:
            for e in ends:
                m = self._create_maze_with_varied_entrances(s, e)
                m.solver = Chain()
                m.solve()

                for sol in m.solutions:
                    self.assertFalse(self._duplicates_in_solution(sol))
                    self.assertTrue(self._one_away(m.start, sol[0]))
                    self.assertTrue(self._one_away(m.end, sol[-1]))

    def test_collision(self):
        """ test against a maze with outer/inner entraces """
        starts = [True, False]
        ends = [True, False]

        for s in starts:
            for e in ends:
                m = self._create_maze_with_varied_entrances(s, e)
                m.solver = Collision()
                m.solve()

                for sol in m.solutions:
                    self.assertFalse(self._duplicates_in_solution(sol))
                    self.assertTrue(self._one_away(m.start, sol[0]))
                    self.assertTrue(self._one_away(m.end, sol[-1]))

    def test_random_mouse(self):
        """ test against a maze with outer/inner entraces """
        starts = [True, False]
        ends = [True, False]

        for s in starts:
            for e in ends:
                m = self._create_maze_with_varied_entrances(s, e)
                m.solver = RandomMouse()
                m.solve()

                for sol in m.solutions:
                    self.assertFalse(self._duplicates_in_solution(sol))
                    self.assertTrue(self._one_away(m.start, sol[0]))
                    self.assertTrue(self._one_away(m.end, sol[-1]))

    def test_shortest_path(self):
        """ test against a maze with outer/inner entraces """
        starts = [True, False]
        ends = [True, False]

        for s in starts:
            for e in ends:
                m = self._create_maze_with_varied_entrances(s, e)
                m.solver = ShortestPath()
                m.solve()

                for sol in m.solutions:
                    self.assertFalse(self._duplicates_in_solution(sol))
                    self.assertTrue(self._one_away(m.start, sol[0]))
                    self.assertTrue(self._one_away(m.end, sol[-1]))

    def test_shortest_paths(self):
        """ test against a maze with outer/inner entraces """
        starts = [True, False]
        ends = [True, False]

        for s in starts:
            for e in ends:
                m = self._create_maze_with_varied_entrances(s, e)
                m.solver = ShortestPaths()
                m.solve()

                for sol in m.solutions:
                    self.assertFalse(self._duplicates_in_solution(sol))
                    self.assertTrue(self._one_away(m.start, sol[0]))
                    self.assertTrue(self._one_away(m.end, sol[-1]))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
