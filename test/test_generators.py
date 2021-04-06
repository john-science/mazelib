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
        assert m.generator.h == 3
        assert m.generator.w == 3
        assert m.generator.H == 7
        assert m.generator.W == 7

        # example 2 of maze dimension definitions
        m.generator = Prims(24, 12)
        assert m.generator.h == 24
        assert m.generator.w == 12
        assert m.generator.H == 49
        assert m.generator.W == 25

        # ensure assertions are failed when invalid maze dimensions are provided
        self.assertRaises(AssertionError, Prims, 2, 2)
        self.assertRaises(AssertionError, Prims, 0, 2)
        self.assertRaises(AssertionError, Prims, -2, 3)
        self.assertRaises(AssertionError, Prims, 224, -2)

    def test_aldous_broder(self):
        """ test the AlgousBroder method generates a reasonably sane maze """
        m = Maze()
        m.generator = AldousBroder(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_backtracking_generator(self):
        """ test the Backtracking method generates a reasonably sane maze """
        m = Maze()
        m.generator = BacktrackingGenerator(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_binary_tree(self):
        """ test the Binary Tree method generates a reasonably sane maze """
        # try without a skew parameter
        m = Maze()
        m.generator = BinaryTree(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

        # try with a skew parameter
        m = Maze()
        m.generator = BinaryTree(4, 5, 'NW')
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_cellular_automaton(self):
        """ test the Cellulator Automaton method generates a reasonably sane maze """
        m = Maze()
        m.generator = CellularAutomaton(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)

    def test_division(self):
        """ test the Division method generates a reasonably sane maze """
        m = Maze()
        m.generator = Division(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_dungeon_rooms_grid(self):
        """ test Dungeon Rooms maze-creation mazes a reasonably sane maze """
        g = np.ones((7, 7), dtype=np.int8)
        g[1] = [1, 1, 1, 1, 1, 1, 1]
        g[2] = [1, 1, 1, 1, 1, 1, 1]
        g[3] = [1, 1, 0, 0, 0, 1, 1]
        g[4] = [1, 1, 0, 0, 0, 1, 1]
        g[5] = [1, 1, 0, 0, 0, 1, 1]

        m = Maze()
        m.generator = DungeonRooms(4, 4, grid=g)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)

    def test_dungeon_reconnect_maze(self):
        """ test Dungeon Rooms maze-creation mazes a reasonably sane maze when reconnecting a maze """
        g = np.ones((7, 7), dtype=np.int8)
        g[1] = [1, 0, 0, 0, 1, 0, 1]
        g[2] = [1, 0, 1, 1, 1, 0, 1]
        g[3] = [1, 0, 0, 0, 1, 0, 1]
        g[4] = [1, 0, 0, 0, 1, 0, 1]
        g[5] = [1, 0, 0, 0, 1, 0, 1]

        m = Maze()
        m.generator = DungeonRooms(4, 4, grid=g)
        m.generator.reconnect_maze()

        assert boundary_is_solid(m.generator.grid)
        assert all_passages_open(m.generator.grid)

    def test_dungeon_rooms_random_rooms(self):
        """ test Dungeon Rooms maze-creation mazes a reasonably sane maze when generating some random rooms """
        m = Maze()
        m.generator = DungeonRooms(4, 4, rooms=[[(1, 1), (3, 3)]], hunt_order='random')
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)

    def test_dungeon_rooms_serpentine_rooms(self):
        """ test DungeonRooms mazes are reasonably when generating some random rooms in a serpentine fashion """
        m = Maze()
        m.generator = DungeonRooms(4, 4, rooms=[[(1, 1), (3, 3)]], hunt_order='serpentine')
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)

    def test_ellers(self):
        """ test the Ellers method generates a reasonably sane maze """
        m = Maze()
        m.generator = Ellers(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_growing_tree(self):
        """ test the Growing Tree method generates a reasonably sane maze """
        m = Maze()
        m.generator = GrowingTree(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_hunt_and_kill_random_order(self):
        """ test the Hunt and Kill method generates a reasonably sane maze, using the random order pathway """
        m = Maze()
        m.generator = HuntAndKill(4, 5, 'random')
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_hunt_and_kill_serpentine_order(self):
        """ test the Hunt and Kill method generates a reasonably sane maze, using the serpentine pathway """
        m = Maze()
        m.generator = HuntAndKill(4, 5, 'serpentine')
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_kruskal(self):
        """ test the Kruskal method generates a reasonably sane maze """
        m = Maze()
        m.generator = Kruskal(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_prims(self):
        """ test the Prims method generates a reasonably sane maze """
        m = Maze()
        m.generator = Prims(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_sidewinder(self):
        """ test the Sidewinder method generates a reasonably sane maze """
        m = Maze()
        m.generator = Sidewinder(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_trivial_maze_spiral(self):
        """ test that the trivial/spiral maze is reasonably sane """
        m = Maze()
        m.generator = TrivialMaze(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)
        assert all_corners_complete(m.grid)

    def test_trivial_maze_serpentine(self):
        """ test that the trivial/spiral maze is reasonably sane when using the serpentine alternative
        run this test enough times to trip the different skewness parameters
        """
        for _ in range(10):
            m = Maze()
            m.generator = TrivialMaze(4, 5, 'serpentine')
            m.generate()

            assert boundary_is_solid(m.grid)
            assert all_passages_open(m.grid)
            assert all_corners_complete(m.grid)

    def test_wilsons_random_order(self):
        """ test the Wilson method generates a reasonably sane maze, using the random order pathway """
        m = Maze()
        m.generator = Wilsons(4, 5, hunt_order='random')
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_wilsons_serpentine_order(self):
        """ test the Wilson method generates a reasonably sane maze, using the serpentine pathway """
        m = Maze()
        m.generator = Wilsons(4, 5, hunt_order='serpentine')
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)


def boundary_is_solid(grid):
    """ Helper method to test of the maze is sane
    Algorithms should generate a maze with a solid boundary of walls.

    Args:
        grid (np.array): maze array
    Returns:
        boolean: is the maze boundary solid?
    """
    # first row
    for c in grid[0]:
        if c == 0:
            return False

    # other rows
    for row in grid[1: -1]:
        if row[0] == 0 or row[-1] == 0:
            return False

    # last row
    for c in grid[grid.shape[0] - 1]:
        if c == 0:
            return False

    return True


def all_passages_open(grid):
    """ Helper method to test of the maze is sane
    All of the (odd, odd) grid cells in a maze should be passages.

    Args:
        grid (np.array): maze array
    Returns:
        booean: Are all the odd/odd grid cells open?
    """
    H, W = grid.shape

    for r in range(1, H, 2):
        for c in range(1, W, 2):
            if grid[r, c] == 1:
                return False

    return True


def all_corners_complete(grid):
    """ Helper method to test of the maze is sane
    All of the (even, even) grid cells in a maze should be walls.

    Args:
        grid (np.array): maze array
    Returns:
        boolean: Are all of the grid corners solid?
    """
    H, W = grid.shape

    for r in range(2, H, 2):
        for c in range(2, W, 2):
            if grid[r, c] == 0:
                return False

    return True


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
