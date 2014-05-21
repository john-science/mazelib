# mazelib

#### A Python API for creating and solving mazes.  --  WORK IN PROGRESS

## The mazelib API

The mazelib library supports Python versions 2.6.x, 2.7.x, and 3.x.

### Generating Mazes

    from mazelib import *

    m = Maze()
    m.generator = Prims(27, 34)
    m.generate()

### Solving Mazes

    m.solver = WallFollower()
    m.generate_entrances()
    m.solve()

## The Algorithms

There are many algorithms for generating and solving mazes. And the implementation in this library have many optional parameters. To learn more, look in the documentation:

#### [Maze-Generating Algorithms](MAZE_GEN_ALGOS.md)

#### [Maze-Solving Algorithms](MAZE_SOLVE_ALGOS.md)


## Examples

How would you display the mazes you generate? In what fun ways can you abuse this library? This is the place to find out.

#### [mazelib Examples and Tricks](EXAMPLES.md)

