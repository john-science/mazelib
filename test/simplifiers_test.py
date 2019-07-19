
import numpy as np
import unittest
from mazelib.mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.simplify.CuldeSacFiller import CuldeSacFiller
from mazelib.simplify.DeadEndFiller import DeadEndFiller


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

        m.simplifiers = [CuldeSacFiller()]
        m.simplify()

        assert m.grid[(1, 5)] == 1

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

        m.simplifiers = [CuldeSacFiller(), DeadEndFiller(99)]
        m.simplify()

        assert m.grid[(1, 5)] == 1
        assert m.grid[(1, 2)] == 1
        assert m.grid[(3, 3)] == 1


def main():
    unittest.main()


if __name__ == '__main__':
    main()
