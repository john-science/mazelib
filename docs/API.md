# mazelib API

##### Go back to the main [README](../README.md)

The `mazelib` library provides tools for creating and solving 2D mazes in Python. The library includes all of the classic algorithms for creating and solving mazes. Most of these have optional parameters to customize the result. Several more modern methods are also provided, to help expedite practical use-cases.

The mazelib library supports Python versions 3.3 and up.


## How to Create a Maze

Let us look at the simplest example:

    from mazelib import *

    m = Maze()
    m.generator = Prims(27, 34)
    m.generate()

First, there was the obligatory import statement, to include mazelib in your Python code: `from mazelib import *`.

Then, a `Maze` object was created. Maze objects have the following attributes:

 * grid: 2D array of data representing the maze itself
 * start: starting location in the maze
 * end: exit location in the maze
 * generator: algorithm used to generate the maze walls
 * solver: algorithm used to solve the maze
 * solutions: list of solution paths to the maze

Finally, an algorithm was selected to generate the maze. In this case, the `Prims` algorithm was used to generate a maze that was 27 rows tall and 34 rows wide. And the Prims algorithm was run.

A complete listing of available maze-generating algorithms can be found [here](MAZE_GEN_ALGOS.md).


## How to Solve a Maze

Again, let's look at the simplest example:

    m.solver = WallFollower()
    m.generate_entrances()
    m.solve()

The `WallFollower` algorithm was choosen to solve the maze. But first, entrances to the maze had to be randomly generated using the helper method `generate_entrances()`. If you prefer, you can manually set the entrances using:

    m.start = (1, 1)
    m.end = (5, 5)

By default, entrances will be generated on the outer edge of the maze. However, you can set if each entrance will be on the outer edge or inside the maze using the optional inputs:

    m.generate_entrances(False, True)
    m.generate_entrances(start_outer=False, end_outer=False)

Finally, the maze `m` was solved for the given entrances, using the `WallFollower` algorithm.

A complete listing of available maze-solving algorithms can be found [here](MAZE_SOLVE_ALGOS.md).


## Advanced: The Monte Carlo Method

A common desire is to not to create just *any* maze but one of a particular difficulty level. The Monte Carlo method can be used to solve these problems.

The idea is simple: a number of equally-sized mazes are generated and solved, then these mazes are organized by the length of their shortest solution. To get a very hard maze, just select one of the ones at the end of the list.

Let us do an example:

    m = Maze()
    m.generator = Prims(50, 51)
    m.solver = WallFollower()
    m.generate_monte_carlo(100, 10, 1.0)

The above code will generate 100 different mazes, and for each maze generate 10 different pairs of start/end entrances (on the outermost border of the maze). For each of the 10 pairs of entrances, one will be selected that generates the longest solution. Then the 100 mazes will be organized by the length of their solutions. In this case, the maze with the longest solution, as defined by the `1.0`, will be returned. If you wanted the maze with the shortest, and hence easiest, solution you would put `m.generate_monte_carlo(100, 10, 0.0)`.  A value of `0.5` would give you a maze with middle-of-the-road difficulty, and so on.

This basic implementation of the Monte Carlo method gives you a lot of power to not just generate mazes, but generate mazes with properties you like.


##### Go back to the main [README](../README.md)
