# mazelib

#### A Python API for creating and solving mazes.  --  WORK IN PROGRESS

## The mazelib API

### Generating Mazes

    from mazelib import *

    m = Maze()
    m.generator = Prims()
    m.generate(27, 34)

### Solving Mazes

    m.solver = DFS()
    m.generate_entrances()
    m.solve()

## The Algorithms

### Maze-Generating Algorithms

#### Aldous-Broder

###### The Algorithm

1. Choose a random vertex.
2. Choose a random neighbor of the vertex and travel to it. If the neighbor has not yet been visited, add the traveled edge to the spanning tree.
3. Repeat step 2 until all vertexes have been visited.

###### Notes

Results: perfect, unbiased

This is one of the slowest maze-generating algorithms. But it produces nice mazes.

The Aldous-Broder algorithm treats the cells of a maze as a graph, and solves to find a Uniform Spanning Tree that covers that graph.

#### Binary Tree

###### The Algorithm

1. For every cell in the grid, knock down a wall either North or West.

It does not matter what order you go through all the cells in the grid. And if you are on the North edge of the grid, you will have to carve West.

###### Notes

Results: perfect, heavily biased

This algorithm produces mazes with a serious flaw: the North and West borders of the maze are completely open. This makes solving the maze too easy to be fun. That is, unless the person solving the maze can't see the whole thing at one time. In which case, this algorithm is still useful.

On the positive side, this algorithm is extremely fast and very easy to implement.

#### Cellular Automaton

###### The Algorithm



###### Notes



#### Eller's

###### The Algorithm



###### Notes



#### Growing Tree

###### The Algorithm

1. Let C be a list of cells, initially empty. Add one cell to C, at random.
2. Choose a cell from C, and carve a passage to any unvisited neighbor of that cell, adding that neighbor to C as well. If there are no unvisited neighbors, remove the cell from C.
3. Repeat #2 until C is empty.

###### Notes



#### Hunt-and-Kill

###### The Algorithm



###### Notes



#### Kruskal's

###### The Algorithm

1. Create a set of all walls in the grid.
2. Randomly select a wall from the grid. If that wall connects two disjoint trees, join the trees. Otherwise, throw that wall away.
3. Repeat #2 until there are no more walls left in the set.

###### Notes

Results: perfect, unbiased

Like Prim's, it is based a namesake algorithm for finding a Minimal Spanning Tree (MST) over a graph.

#### Monte Carlo

###### The Algorithm



###### Notes

There's an old joke that particle physicists use Monte Carlo modeling to solve all their problems: where to eat lunch, finding love, everything.

Well, I guess I was at Fermliab too long. This is an original algorithm, using the first algorithm I ever learned in software. (I may work on creating a Las Vegas algorithm variation).

#### Prim's

###### The Algorithm

1. Choose an arbitrary cell from the grid, and add it to some (initially empty) set visited nodes (V).
2. Randomly select a wall from the grid, that connects a cell in V with another cell not in V.
3. Add that wall to the Minimal Spanning Tree (MST), and the edge’s other cell to V.
4. Repeat steps 2 and 3 until V includes every cell in G.

###### Notes

Results: perfect, unbiased

This is a classic. Like Kruskal's, it is based on the idea of finding a MST in a graph. But Prim's is purely random. In fact, randomized variations on other maze-generating algorithms are frequently called "Prim's variations".

#### Recursive Backtracker

###### The Algorithm

1. Randomly select a starting cell.
2. Randomly choose a wall at that cell and carve a passage through to the adjacent cell, but only if the adjacent cell has not been visited yet. This becomes the new current cell.
3. If all adjacent cells have been visited, back up to the last cell that has uncarved walls and repeat.
4. The algorithm ends when the process has backed all the way up to the starting cell.

###### Notes

Results: perfect, unbiased

This is a standard maze-generation algorithm because it is easy to understand and implement. And it produces high-quality mazes.

#### Recursive Division

###### The Algorithm



###### Notes



#### Sidewinder

###### The Algorithm



###### Notes

Results: perfect, biased




#### Wilson's

###### The Algorithm



###### Notes





### Maze-Soliving Algorithms

## Using the Results

For the rest of this section, let us assume we have already generated a maze:

    from mazelib import *

    m = Maze()
    m.generator = Prims()
    m.generate(27, 34)

#### Example 1: Plotting the Maze in Plain Text

It is helpful to have a low-key, fast way to print out mazes (and solutions) as you develop. I typically use this one:

    def tostr(grid):
        """Return a string representation of the maze."""
        txt = ''
        for row in grid:
            for cell in row:
                txt += '#' if cell else ' '
            txt += '\n'
    
        return txt
        
    print tostr(m.grid)

#### Example 2: Plotting the Maze with Matplotlib

Sometimes it is hard to see the finer points of a maze unless it is a graphic.  You want to see at a moment's glance if the maze has unreachable sections, if it is obviously too easy, if it is large enough to meet your needs, etcetera.



#### Example 3: Displaying the Maze as CSS

Just a simple function to draw a maze in CSS/HTML. The benefit here is you don't need any special Python libraries. And CSS is really easy to fine-tune to customize the final output.



#### Example 4: Drawing the Maze with XKCD style

Let's have some fun with it. And chances are, if you're reading this you probably like XKCD.


## Vocabulary

1. biased - 
2. cell - 
3. grid - 
4. perfect - a maze is perfect if it has one and only one solution
5. wall - 
