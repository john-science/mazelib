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

## How to Solve a Maze

Again, the simplest example is:

    m.solver = WallFollower()
    m.generate_entrances()
    m.solve()
    
Now, let's look at what we did.

DOCUMENTION INCOMING

## Advanced: The Monte Carlo Method

Let us say you want to generate the hardest possible maze (of a given size). Or you want to generate a whole sequence of mazes of increasing difficulty. In the past, this would be a heavily manual process.

DOCUMENTION INCOMING


#####Go back to the main [README](../README.md)
