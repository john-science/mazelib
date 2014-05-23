# mazelib Examples

#####Go back to the main [README](../README.md)


## Displaying the Results

For the rest of this section, let us assume we have already generated a maze:

    from mazelib import *

    m = Maze()
    m.generator = Prims(27, 34)
    m.generate()
