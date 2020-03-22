
import numpy as np
import unittest
from mazelib.mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.generate.TrivialMaze import TrivialMaze
from mazelib.transmute.CuldeSacFiller import CuldeSacFiller
from mazelib.transmute.DeadEndFiller import DeadEndFiller
from mazelib.transmute.Perturbation import Perturbation
from .test_generators import all_corners_complete, all_passages_open, boundary_is_solid


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

    def test_cul_de_sac_filler(self):
        m = Maze()
        m.generator = Prims(3, 3)
        m.generate()
        m.grid = self._example_cul_de_sac_maze()

        assert m.grid[(1, 5)] == 0

        m.transmuters = [CuldeSacFiller()]
        m.transmute()

        assert m.grid[(1, 5)] == 1

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_corners_complete(m.grid))

    def test_dead_end_filler(self):
        m = Maze()
        m.generator = Prims(3, 3)
        m.generate()
        m.start = (1, 0)
        m.end = (5, 6)
        m.grid = self._example_cul_de_sac_maze()

        assert m.grid[(1, 5)] == 0
        assert m.grid[(1, 2)] == 0
        assert m.grid[(3, 3)] == 0

        m.transmuters = [CuldeSacFiller(), DeadEndFiller(99)]
        m.transmute()

        assert m.grid[(1, 5)] == 1
        assert m.grid[(1, 2)] == 1
        assert m.grid[(3, 3)] == 1

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_corners_complete(m.grid))

    def test_perturbation(self):
        m = Maze()
        m.generator = TrivialMaze(4, 5)
        m.generate()

        m.transmuters = [Perturbation()]
        m.transmute()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))
        self.assertTrue(all_corners_complete(m.grid))


if __name__ == '__main__':
    unittest.main()  #argv=['first-arg-is-ignored'], exit=False)

