import numpy as np
import unittest
from mazelib.mazelib import Maze
from mazelib.generate.AldousBroder import AldousBroder
from mazelib.generate.BacktrackingGenerator import BacktrackingGenerator
from mazelib.generate.BinaryTree import BinaryTree
from mazelib.generate.CellularAutomaton import CellularAutomaton
from mazelib.generate.Division import Division
from mazelib.generate.DungeonRooms import DungeonRooms
from mazelib.generate.Ellers import Ellers
from mazelib.generate.GrowingTree import GrowingTree
from mazelib.generate.HuntAndKill import HuntAndKill
from mazelib.generate.Kruskal import Kruskal
from mazelib.generate.Prims import Prims
from mazelib.generate.Sidewinder import Sidewinder
from mazelib.generate.TrivialMaze import TrivialMaze
from mazelib.generate.Wilsons import Wilsons


class GeneratorsTest(unittest.TestCase):

    def test_abstract_constructor(self):
        """ test the MazeGenAlgo constructor """
        # example 1 of maze dimension definitions
        m = Maze()
        m.generator = Prims(3, 3)
        self.assertEqual(m.generator.h, 3)
        self.assertEqual(m.generator.w, 3)
        self.assertEqual(m.generator.H, 7)
        self.assertEqual(m.generator.W, 7)

        # example 2 of maze dimension definitions
        m.generator = Prims(24, 12)
        self.assertEqual(m.generator.h, 24)
        self.assertEqual(m.generator.w, 12)
        self.assertEqual(m.generator.H, 49)
        self.assertEqual(m.generator.W, 25)

        # ensure assertions are failed when invalid maze dimensions are provided
        self.assertRaises(AssertionError, Prims, 2, 2)
        self.assertRaises(AssertionError, Prims, 0, 2)
        self.assertRaises(AssertionError, Prims, -2, 3)
        self.assertRaises(AssertionError, Prims, 224, -2)

    def test_aldous_broder(self):
        m = Maze()
        m.generator = AldousBroder(4, 5)
        m.generate()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))
        self.assertTrue(all_corners_complete(m.grid))

    def test_backtracking_generator(self):
        m = Maze()
        m.generator = BacktrackingGenerator(4, 5)
        m.generate()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))
        self.assertTrue(all_corners_complete(m.grid))

    def test_binary_tree(self):
        m = Maze()
        m.generator = BinaryTree(4, 5)
        m.generate()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))
        self.assertTrue(all_corners_complete(m.grid))

    def test_cellular_automaton(self):
        m = Maze()
        m.generator = CellularAutomaton(4, 5)
        m.generate()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))

    def test_division(self):
        m = Maze()
        m.generator = Division(4, 5)
        m.generate()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))
        self.assertTrue(all_corners_complete(m.grid))

    def test_dungeon_rooms_grid(self):
        g = np.ones((7, 7), dtype=np.int8)
        g[1] = [1,1,1,1,1,1,1]
        g[2] = [1,1,1,1,1,1,1]
        g[3] = [1,1,0,0,0,1,1]
        g[4] = [1,1,0,0,0,1,1]
        g[5] = [1,1,0,0,0,1,1]

        m = Maze()
        m.generator = DungeonRooms(4, 4, grid=g)
        m.generate()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))

    def test_dungeon_reconnect_maze(self):
        g = np.ones((7, 7), dtype=np.int8)
        g[1] = [1,0,0,0,1,0,1]
        g[2] = [1,0,1,1,1,0,1]
        g[3] = [1,0,0,0,1,0,1]
        g[4] = [1,0,0,0,1,0,1]
        g[5] = [1,0,0,0,1,0,1]

        m = Maze()
        m.generator = DungeonRooms(4, 4, grid=g)
        m.generator.reconnect_maze()

        self.assertTrue(boundary_is_solid(m.generator.grid))
        self.assertTrue(all_passages_open(m.generator.grid))

    def test_dungeon_rooms_random_rooms(self):
        m = Maze()
        m.generator = DungeonRooms(4, 4, rooms=[[(1,1), (3,3)]], hunt_order='random')
        m.generate()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))

    def test_dungeon_rooms_serpentine_rooms(self):
        m = Maze()
        m.generator = DungeonRooms(4, 4, rooms=[[(1,1), (3,3)]], hunt_order='serpentine')
        m.generate()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))

    def test_ellers(self):
        m = Maze()
        m.generator = Ellers(4, 5)
        m.generate()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))
        self.assertTrue(all_corners_complete(m.grid))

    def test_growing_tree(self):
        m = Maze()
        m.generator = GrowingTree(4, 5)
        m.generate()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))
        self.assertTrue(all_corners_complete(m.grid))

    def test_hunt_and_kill_random_order(self):
        m = Maze()
        m.generator = HuntAndKill(4, 5, 'random')
        m.generate()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))
        self.assertTrue(all_corners_complete(m.grid))

    def test_hunt_and_kill_serpentine_order(self):
        m = Maze()
        m.generator = HuntAndKill(4, 5, 'serpentine')
        m.generate()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))
        self.assertTrue(all_corners_complete(m.grid))

    def test_kruskal(self):
        m = Maze()
        m.generator = Kruskal(4, 5)
        m.generate()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))
        self.assertTrue(all_corners_complete(m.grid))

    def test_prims(self):
        m = Maze()
        m.generator = Prims(4, 5)
        m.generate()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))
        self.assertTrue(all_corners_complete(m.grid))

    def test_sidewinder(self):
        m = Maze()
        m.generator = Sidewinder(4, 5)
        m.generate()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))
        self.assertTrue(all_corners_complete(m.grid))

    def test_trivial_maze_spiral(self):
        m = Maze()
        m.generator = TrivialMaze(4, 5)
        m.generate()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))
        self.assertTrue(all_corners_complete(m.grid))
        self.assertTrue(all_corners_complete(m.grid))

    def test_trivial_maze_serpentine(self):
        # run this test enough times to trip the different skewness parameters
        for _ in range(10):
            m = Maze()
            m.generator = TrivialMaze(4, 5, 'serpentine')
            m.generate()

            self.assertTrue(boundary_is_solid(m.grid))
            self.assertTrue(all_passages_open(m.grid))
            self.assertTrue(all_corners_complete(m.grid))

    def test_wilsons_random_order(self):
        m = Maze()
        m.generator = Wilsons(4, 5, hunt_order='random')
        m.generate()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))
        self.assertTrue(all_corners_complete(m.grid))

    def test_wilsons_serpentine_order(self):
        m = Maze()
        m.generator = Wilsons(4, 5, hunt_order='serpentine')
        m.generate()

        self.assertTrue(boundary_is_solid(m.grid))
        self.assertTrue(all_passages_open(m.grid))
        self.assertTrue(all_corners_complete(m.grid))


def boundary_is_solid(grid):
    """ Algorithms should generate a maze with a solid boundary of walls. """
    # first row
    for c in grid[0]:
        if c == 0:
            return False

    # other rows
    for row in grid[1: -1]:
        if row[0] == 0 or row[-1] == 0:
            return False

    # last row
    for c in grid[grid.shape[0]-1]:
        if c == 0:
            return False

    return True


def all_passages_open(grid):
    """ All of the (odd, odd) grid cells in a maze should be passages. """
    H, W = grid.shape

    for r in range(1, H, 2):
        for c in range(1, W, 2):
            if grid[r, c] == 1:
                return False

    return True


def all_corners_complete(grid):
    """ All of the (even, even) grid cells in a maze should be walls. """
    H, W = grid.shape

    for r in range(2, H, 2):
        for c in range(2, W, 2):
            if grid[r, c] == 0:
                return False

    return True


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

