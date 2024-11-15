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
        """Test the MazeGenAlgo constructor."""
        # example 1 of maze dimension definitions
        m = Maze(723)
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
        """Test the AlgousBroder method generates a reasonably sane maze."""
        m = Maze(143)
        m.generator = AldousBroder(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_backtracking_generator(self):
        """Test the Backtracking method generates a reasonably sane maze."""
        m = Maze(23)
        m.generator = BacktrackingGenerator(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_binary_tree(self):
        """Test the Binary Tree method generates a reasonably sane maze."""
        # try without a skew parameter
        m = Maze(163)
        m.generator = BinaryTree(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

        # try with a skew parameter
        m = Maze(1298)
        m.generator = BinaryTree(4, 5, "NW")
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_cellular_automaton(self):
        """Test the Cellulator Automaton method generates a reasonably sane maze."""
        m = Maze(183)
        m.generator = CellularAutomaton(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)

    def test_division(self):
        """Test the Division method generates a reasonably sane maze."""
        m = Maze(653)
        m.generator = Division(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_dungeon_rooms_grid(self):
        """Test Dungeon Rooms maze-creation mazes a reasonably sane maze."""
        g = np.ones((7, 7), dtype=np.int8)
        g[1] = [1, 1, 1, 1, 1, 1, 1]
        g[2] = [1, 1, 1, 1, 1, 1, 1]
        g[3] = [1, 1, 0, 0, 0, 1, 1]
        g[4] = [1, 1, 0, 0, 0, 1, 1]
        g[5] = [1, 1, 0, 0, 0, 1, 1]

        m = Maze(1293)
        m.generator = DungeonRooms(4, 4, grid=g)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)

    def test_dungeon_reconnect_maze(self):
        """Test Dungeon Rooms maze-creation mazes a reasonably sane maze when reconnecting a maze."""
        g = np.ones((7, 7), dtype=np.int8)
        g[1] = [1, 0, 0, 0, 1, 0, 1]
        g[2] = [1, 0, 1, 1, 1, 0, 1]
        g[3] = [1, 0, 0, 0, 1, 0, 1]
        g[4] = [1, 0, 0, 0, 1, 0, 1]
        g[5] = [1, 0, 0, 0, 1, 0, 1]

        m = Maze(865)
        m.generator = DungeonRooms(4, 4, grid=g)
        m.generator.reconnect_maze()

        assert boundary_is_solid(m.generator.grid)
        assert all_passages_open(m.generator.grid)

    def test_dungeon_rooms_random_rooms(self):
        """Test Dungeon Rooms maze-creation mazes a reasonably sane maze when generating some random rooms."""
        for i in range(20):
            m = Maze(900 + i)
            m.generator = DungeonRooms(
                4, 4, rooms=[[(1, 1), (3, 3)]], hunt_order="random"
            )
            m.generate()

            assert boundary_is_solid(m.grid)
            assert all_passages_open(m.grid)

    def test_dungeon_rooms_serpentine_rooms(self):
        """Test DungeonRooms mazes are reasonably when generating some random rooms in a serpentine fashion."""
        m = Maze(443)
        m.generator = DungeonRooms(
            4, 4, rooms=[[(1, 1), (3, 3)]], hunt_order="serpentine"
        )
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)

    def test_ellers(self):
        """Test the Ellers method generates a reasonably sane maze."""
        m = Maze(563)
        m.generator = Ellers(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_growing_tree(self):
        """Test the Growing Tree method generates a reasonably sane maze."""
        m = Maze(743)
        m.generator = GrowingTree(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_hunt_and_kill_random_order(self):
        """Test the Hunt and Kill method generates a reasonably sane maze, using the random order pathway."""
        m = Maze(8888)
        m.generator = HuntAndKill(4, 5, "random")
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_hunt_and_kill_serpentine_order(self):
        """Test the Hunt and Kill method generates a reasonably sane maze, using the serpentine pathway."""
        m = Maze(808)
        m.generator = HuntAndKill(4, 5, "serpentine")
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_kruskal(self):
        """Test the Kruskal method generates a reasonably sane maze."""
        m = Maze(314)
        m.generator = Kruskal(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_prims(self):
        """Test the Prims method generates a reasonably sane maze."""
        m = Maze(159)
        m.generator = Prims(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_sidewinder(self):
        """Test the Sidewinder method generates a reasonably sane maze."""
        m = Maze(26)
        m.generator = Sidewinder(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_trivial_maze_spiral(self):
        """Test that the trivial/spiral maze is reasonably sane."""
        m = Maze(535)
        m.generator = TrivialMaze(4, 5)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)
        assert all_corners_complete(m.grid)

    def test_trivial_maze_serpentine(self):
        """Test that the trivial/spiral maze is reasonably sane when using the serpentine alternative
        run this test enough times to trip the different skewness parameters.
        """
        for i in range(20):
            m = Maze(1967 + i)
            m.generator = TrivialMaze(4, 5, "serpentine")
            m.generate()

            assert boundary_is_solid(m.grid)
            assert all_passages_open(m.grid)
            assert all_corners_complete(m.grid)

    def test_wilsons_random_order(self):
        """Test the Wilson method generates a reasonably sane maze, using the random order pathway."""
        m = Maze(432)
        m.generator = Wilsons(4, 5, hunt_order="random")
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)

    def test_wilsons_serpentine_order(self):
        """Test the Wilson method generates a reasonably sane maze, using the serpentine pathway."""
        m = Maze(12345)
        m.generator = Wilsons(4, 5, hunt_order="serpentine")
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        assert all_corners_complete(m.grid)


def boundary_is_solid(grid):
    """Helper method to test of the maze is sane.
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
    for row in grid[1:-1]:
        if row[0] == 0 or row[-1] == 0:
            return False

    # last row
    for c in grid[grid.shape[0] - 1]:
        if c == 0:
            return False

    return True


def all_passages_open(grid):
    """Helper method to test of the maze is sane.
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
    """Helper method to test of the maze is sane.
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


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
