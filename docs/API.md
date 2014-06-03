# mazelib API

#####Go back to the main [README](../README.md)

The mazelib library is a general library for creating and solving mazes in Python. The library includes all of the classic algorithms for creating and solving mazes, as well as variations on these. Several more modern methods for generating and solving mazes are also provided, to help expedite the practical uses of mazes.

The mazelib library supports Python versions 2.5.x, 2.6.x, 2.7.x, and 3.x.

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

Let us say you want to generate the hardest possible maze (of a given size). Or you want to generate a whole sequence of mazes of increasing difficulty. In the past, this would be a heavily manual process.

DOCUMENTION INCOMING


#####Go back to the main [README](../README.md)
