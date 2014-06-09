# mazelib API

#####Go back to the main [README](../README.md)

The mazelib library is a general library for creating and solving mazes in Python. The library includes all of the classic algorithms for creating and solving mazes, as well as variations on these. Several more modern methods for generating and solving mazes are also provided, to help expedite the practical uses of mazes.

The mazelib library supports Python versions 2.5.x, 2.6.x, 2.7.x, and will soon support 3.x.

## How to Create a Maze

The simplest example is:

    from mazelib import *

    m = Maze()
    m.generator = Prims(27, 34)
    m.generate()

So, what did we do there?

First, there was the obligatory import statment, to include mazelib in your Python code 'from mazelib import *'.

Then, a `Maze` object was created:

* Maze
 * grid: 2D array of data representing the maze itself
 * start: staring entrance location in the maze
 * end: exit entrance location in the maze
 * generator: algorithm used to generate the maze walls
 * solver: algorithm used to solve the maze
 * solutions: list of solution paths to the maze

Finally, an algorithm was selected to generate the maze, and it was run. In this case, the `Prims` algorithm was used to generate a maze that was 27 rows tall and 34 rows wide.

A complete listing of available maze-generating algorithms can be found [here](MAZE_GEN_ALGOS.md).

## How to Solve a Maze

Again, the simplest example is:

    m.solver = WallFollower()
    m.generate_entrances()
    m.solve()
    
Now, let's look at what we did.

The `WallFollower` algorithm was choosen to solve the maze. But first, entrances to the maze had to be randomly generated using the helper method `generate_entrances()`. Of course, if you prefer, you can manually set the entrances using:

    m.start = (1, 1)
    m.end = (5, 5)

By default, entrances will be generated on the outer edge of the maze. However, if you want the entrances to appear randomly within the maze, you can use the set the flag to `False`:

    m.generate_entrances(False)
    m.generate_entrances(outer=False)

Finally, the solving algorithm was run for the given maze `m`, from the start to the end.

A complete listing of available maze-solving algorithms can be found [here](MAZE_SOLVE_ALGOS.md).

## Advanced: The Monte Carlo Method

When creating a maze, you may want to create a very hard maze, instead of just any old maze. Or you may want to create a whole series of mazes, each progressively harder. These are common goals that used to require a lot of tedious hand-selection. Today, however, these common problems can be solved using the Monte Carlo method.

The idea is simple: a set number of equally-sized mazes are generated and solved, then these mazes are organized by the length of their shortest solution. Now you have a rubric to quantify your "maze difficulty". To get a very hard maze, just select one of the ones at the end of the list.

Let us do an example:

    m = Maze()
    m.generator = Prims(50, 51)
    m.solver = WallFollower()
    m.generate_monte_carlo(100, 10, 1.0)

The above code will generate 100 different mazes, and for each maze generate 10 different pairs of start/end entrances (on the outermost border of the maze). Then it will return the maze with the longest solution, as defined by the `1.0`. If you wanted the maze with the shortest, and hence easiest, solution you would put `0.0` here.  A value of `0.5` would give you a maze with middle-of-the-road difficulty, and so on.

This basic implementation of the Monte Carlo method gives you a lot of power to not just generate mazes, but generate mazes with properties you like.


#####Go back to the main [README](../README.md)
