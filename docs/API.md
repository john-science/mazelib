# mazelib API

#####Go back to the main [README](../README.md)

The mazelib library is a general library to expedite creating and solving mazes in Python. The library includes all of the classic algorithms for creating and solving mazes, as well as variations on all of these. Several more modern methods for generating and solving mazes are also provided, to help expedite the kinds of things that people typically create mazes for.

The mazelib library supports Python versions 2.6.x, 2.7.x, and 3.x.

## How to Create a Maze

The simplest example is:

    from mazelib import *

    m = Maze()
    m.generator = Prims(27, 34)
    m.generate()

So, what did we do there?

DOCUMENTION INCOMING

## How to Solve a Maze

Again, the simplest example is:

    m.solver = WallFollower()
    m.generate_entrances()
    m.solve()
    
Now, let's look at what we did.

DOCUMENTION INCOMING

## Advanced: Using the Monte Carlo Method to Create a Maze of Desired Difficulty

Let us say you want to generate the hardest possible maze (of a given size). Or you want to generate a whole sequence of mazes of increasing difficulty. In the past, this would be a heavily manual process.

DOCUMENTION INCOMING


#####Go back to the main [README](../README.md)
