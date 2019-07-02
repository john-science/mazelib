
import numpy as np
import unittest
from mazelib.generate.Prims import Prims
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
from mazelib.solve.BlindAlley import BlindAlley
from mazelib.solve.Chain import Chain
from mazelib.solve.Collision import Collision
from mazelib.solve.CuldeSacFiller import CuldeSacFiller
from mazelib.solve.DeadEndFiller import DeadEndFiller
from mazelib.solve.RandomMouse import RandomMouse
from mazelib.solve.ShortestPath import ShortestPath
from mazelib.solve.ShortestPaths import ShortestPaths
from mazelib.solve.WallFollower import WallFollower
from mazelib.mazelib import Maze


class SolversTest(unittest.TestCase):
    
    def _example_cul_de_sac_maze(self):
        """
        #######
              #
        # # # #
        # #   #
        # #####
        #
        #######
        """
        g = np.ones((7, 7), dtype=np.int8)
        g[1] = [1,0,0,0,0,0,1]
        g[2] = [1,0,1,0,1,0,1]
        g[3] = [1,0,1,0,0,0,1]
        g[4] = [1,0,1,1,1,1,1]
        g[5] = [1,0,0,0,0,0,1]
    
        return g

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
                    # TODO: Should these below pass for BacktrackingSolver? Or not?
                    #self.assertTrue(self._one_away(m.start, sol[0]))
                    #self.assertTrue(self._one_away(m.end, sol[-1]))

    def test_blind_alley_filler(self):
        """ test BlindAlley against a maze with outer/inner entraces using filler approach """
        starts = [True, False]
        ends = [True, False]

        for s in starts:
            for e in ends:
                m = self._create_maze_with_varied_entrances(s, e)
                m.solver = BlindAlley()
                m.solve()

                for sol in m.solutions:
                    self.assertFalse(self._duplicates_in_solution(sol))
                    self.assertTrue(self._one_away(m.start, sol[0]))
                    self.assertTrue(self._one_away(m.end, sol[-1]))

    def test_blind_alley_sealer(self):
        """ test BlindAlley against a maze with outer/inner entraces using sealer approach """
        starts = [True, False]
        ends = [True, False]

        for s in starts:
            for e in ends:
                m = self._create_maze_with_varied_entrances(s, e)
                m.solver = BlindAlley(fill_type='sealer', solver=Collision())
                m.solve()

                for sol in m.solutions:
                    self.assertFalse(self._duplicates_in_solution(sol))
                    self.assertTrue(self._one_away(m.start, sol[0]))
                    self.assertTrue(self._one_away(m.end, sol[-1]))

    def test_chain_pruned(self):
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

    def test_chain_unpruned(self):
        """ test against a maze with outer/inner entraces """
        starts = [True, False]
        ends = [True, False]

        for s in starts:
            for e in ends:
                m = self._create_maze_with_varied_entrances(s, e)
                m.solver = Chain(prune=False)
                m.solve()

                for sol in m.solutions:
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

    def test_cul_de_sac_filler(self):
        """ test against a maze with outer/inner entraces """
        starts = [True, False]
        ends = [True, False]

        g = self._example_cul_de_sac_maze()

        for s in starts:
            for e in ends:
                m = Maze()
                m.generator = Prims(3, 3)
                m.grid = g

                if s and e:
                    m.start = (1, 0)
                    m.end = (5, 6)
                elif not s and not e:
                    m.start = (1, 1)
                    m.end = (5, 5)
                else:
                    if s:
                        m.start = (1, 1)
                        m.end = (5, 5)
                    else:
                        m.start = (1, 1)
                        m.end = (5, 6)

                m.solver = CuldeSacFiller()
                m.solve()

                for sol in m.solutions:
                    self.assertFalse(self._duplicates_in_solution(sol))
                    self.assertTrue(self._one_away(m.start, sol[0]))
                    self.assertTrue(self._one_away(m.end, sol[-1]))

    def test_dead_end_filler(self):
        """ test DeadEndFiller against a maze with outer/inner entraces """
        starts = [True, False]
        ends = [True, False]

        for s in starts:
            for e in ends:
                m = self._create_maze_with_varied_entrances(s, e)
                m.solver = DeadEndFiller()
                m.solve()

                for sol in m.solutions:
                    self.assertFalse(self._duplicates_in_solution(sol))
                    self.assertTrue(self._one_away(m.start, sol[0]))
                    self.assertTrue(self._one_away(m.end, sol[-1]))

    def test_random_mouse_pruned(self):
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

    def test_random_mouse_unpruned(self):
        """ test against a maze with outer/inner entraces """
        starts = [True, False]
        ends = [True, False]

        for s in starts:
            for e in ends:
                m = self._create_maze_with_varied_entrances(s, e)
                m.solver = RandomMouse(prune=False)
                m.solve()

                for sol in m.solutions:
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

    def test_wall_follower(self):
        """ test against a maze with outer/inner entraces """
        starts = [True, False]
        ends = [True, False]

        for s in starts:
            for e in ends:
                m = self._create_maze_with_varied_entrances(s, e)
                m.solver = WallFollower()
                m.solve()

                for sol in m.solutions:
                    self.assertFalse(self._duplicates_in_solution(sol))
                    self.assertTrue(self._one_away(m.start, sol[0]))
                    self.assertTrue(self._one_away(m.end, sol[-1]))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
