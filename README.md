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

1. Choose a random cell.
2. Choose a random neighbor of the current cell and visit it. If the neighbor has not yet been visited, add the traveled edge to the spanning tree.
3. Repeat step 2 until all cells have been visited.

###### Notes

Results: perfect, unbiased

This is one of the slowest maze-generating algorithms. But it produces nice mazes.

The Aldous-Broder algorithm treats the cells of a maze as a graph, and solves to find a Uniform Spanning Tree that covers that graph.

#### Backtracking

###### The Algorithm

1. Randomly choose a starting cell.
2. Randomly choose a wall at the current cell and open a passage through to any random adjacent cell, that has not been visited yet. This is now the current cell.
3. If all adjacent cells have been visited, back up to the previous and repeat step 2.
4. Stop when the algorithm has backed all the way up to the starting cell.

###### Notes

Results: perfect, unbiased

This is a standard maze-generation algorithm because it is easy to understand and implement. And it produces high-quality mazes.

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

Cells survive if they have one to four neighbours. If a cell has exactly three neighbours, it is born. It is similar to Conway's Game of Life in that patterns that do not have a living cell adjacent to 1, 4, or 5 other living cells in any generation will behave identically to it.

###### Notes

Results: perfect, unbiased

Using Cellular Automation to generate a maze is a really fun idea, and it is even reasonably fast. And the result is a "perfect" maze, but not always the hardest maze. Generating a few of these mazes, you begin to see that the results are frequently quick easy to solve.

More research is needed to create a post-processing step to remove the typical Cellular Automaton defects.

#### Eller's

###### The Algorithm

1. Put each cell in the first row into their own set.
2. Randomly join adjacent cells, but only if they are not in the same set. When joining adjacent cells, merge the cells of both sets into a single set.
3. For each set, randomly create vertical connections downward to the next row. Each remaining set must have at least one vertical connection. The cells in the next row thus connected must share the set of the cell above them.
4. Complete the next row by placing any remaining cells into their own sets.
5. Repeat step 2-4 until the last row.
6. For the last row, join all adjacent cells that do not share a set, and omit the vertical connections.

###### Notes

Results: perfect, unbiased



#### Growing Tree

###### The Algorithm

1. Let C be a list of cells, initially empty. Add one cell to C, at random.
2. Choose a cell from C, and carve a passage to any unvisited neighbor of that cell, adding that neighbor to C as well. If there are no unvisited neighbors, remove the cell from C.
3. Repeat step 2 until C is empty.

###### Notes

Results: perfect, unbiased

This algorithm is very flexible. Instead of defining exactly what must be done, it lays out a general construct. The exact order in which we choose a new cell from set C in step 2 is left undefined. That means we can pick on at random (and mimick the Prim's algorithm), or always pick the most recent one (and mimick the Backtracking algorithm). The implementation here allows the developer to set the percentage of time Backtracking is chosen versus Prim's. This gives a lot of variety to the final complexity and look of the final maze.

#### Hunt-and-Kill

###### The Algorithm

1. Randomly choose a starting cell.
2. Perform a random walk from the current cell, carving passages to unvisited neighbors, until the current cell has no unvisited neighbors.
3. Randomly select a new grid cell, if it has been visited, walk from it.
4. Repeat steps 2 and 3 a sufficient number of times that there the probability of a cell not being visited is extremely small.

###### Notes

Results: perfect, unbiased

Generally, you might think random-walk algorithms are very slow. But Hunt-and-Kill is quite efficient. And I really like the end results of this algorithm, the mazes are not easy to solve.
On a side note, there is a statistical probability that some cells will not be part of the maze with this algorithm. However, the maze would still be perfect.  And the probability of that event is quite small.

#### Kruskal's

###### The Algorithm

1. Create a set of all walls in the grid.
2. Randomly select a wall from the grid. If that wall connects two disjoint trees, join the trees. Otherwise, throw that wall away.
3. Repeat step 2 until there are no more walls left in the set.

###### Notes

Results: perfect, unbiased

Like Prim's, it is based on a namesake algorithm for finding a Minimal Spanning Tree (MST) over a graph.

#### Monte Carlo

###### The Algorithm

TBA

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

#### Recursive Division

###### The Algorithm

1. Start with an empty grid.
2. Bisect the grid with a wall (horizontal or vertical). Add a single passage through the wall.
3. Repeat step 2 with the areas on either side of the wall.
4. Continue, recursively, until the maze passages are the desired resolution.

###### Notes

Results: perfect, biased

The algorithm is very simple to understand, and reasonably simple to implement. But the results will always look skewed. A big line that perfect divides a maze makes it easier for the human eye to solve a maze: we can quickly reduce our search space. This is doubly true for humans that happen to know the maze was created by division.

This implementation tries, as far as is possible, to reduce these biases by alternating the cuts between horizontal and vertical. (Obviously, if you made 7 vertical cuts in a row the maze would be very easy to solve.)


#### Sidewinder

###### The Algorithm

1. Work through the grid row-wise, starting with the cell at 0,0.
2. Add the current cell to a “run” set.
3. For the current cell, randomly decide whether to carve East.
4. If a passage East was carved, make the new cell the current cell and repeat steps 2-4.
5. If a passage East was not carved, choose any one of the cells in the run set and carve a passage North. Then empty the run set. Repeat steps 2-5.
6. Continue until all rows have been processed.

###### Notes

Results: perfect, biased

The algorithm is simple and optimally fast. However, the North side of the maze will always be one, long, open corridor. For my tastes, this makes the maze too easy to solve. There are use-cases where that will not matter though.

Active research is underway to create a post-processing step to fix this bias.


#### Wilson's

###### The Algorithm

1. Choose a random cell and add it to the Uniform Spanning Tree (UST).
2. Select any cell that is not in the UST and perform a random walk until you find a cell that is.
3. Add the cells and walls visited in the random walk to the UST.
4. Repeat steps 2 and 3 until all cells have been added to the UST.

###### Notes

Results: perfect, unbiased

Like all random-walk algorithms, Wilson's isn't terribly fast. However, as UST-based algorithms go, this converges faster than Aldous-Broder.



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

    import matplotlib.pyplot as plt

    def showPNG(grid):
        """Generate a simple image of the maze."""
        walls = []
        for wall in grid:
            walls.append(list(wall))
    
        plt.figure(figsize=(10, 5))
        plt.imshow(walls, cmap=plt.cm.binary, interpolation='nearest')
        plt.xticks([]), plt.yticks([])
        plt.show()

#### Example 3: Displaying the Maze as CSS

Just a simple function to draw a maze in CSS/HTML. The benefit here is you don't need any special Python libraries. And CSS is really easy to fine-tune to customize the final output.

    def toHTML(grid, cell_size=10):
        row_max = grid.height
        col_max = grid.width

        html = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"' + \
               '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">' + \
               '<html xmlns="http://www.w3.org/1999/xhtml"><head>' + \
               '<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />' + \
               '<style type="text/css" media="screen">' + \
               '#maze {width: ' + str(cell_size * col_max) + 'px;height: ' + \
               str(cell_size * row_max) + 'px;border: 3px solid grey;}' + \
               'div.maze_row div{width: ' + str(cell_size) + 'px;height: ' + str(cell_size) + 'px;}' + \
               'div.maze_row div.bl{background-color: black;}' + \
               'div.maze_row div.wh{background-color: white;}' + \
               'div.maze_row div{float: left;}' + \
               'div.maze_row:after{content: ".";height: 0;visibility: hidden;display: block;clear: both;}' + \
               '</style></head><body>' + \
               '<div id="maze">'

        for row in xrange(row_max):
            html += '<div class="maze_row">'
            for col in xrange(col_max):
                if grid[row][col]:
                    html += '<div class="bl"></div>'
                else:
                    html += '<div class="wh"></div>'
            html += '</div>'
        html += '</div></body></html>'
        
        return html

#### Example 4: Drawing the Maze with XKCD style

Let's have some fun with it. And chances are, if you're reading this you probably like XKCD.

    import numpy as np
    from matplotlib.path import Path
    from matplotlib.patches import PathPatch
    import matplotlib.pyplot as plt
    
    def plotXKCD(grid):
        """ Generate an XKCD-styled line-drawn image of the maze. """
        H = len(grid)
        W = len(grid[0])
        h = (H - 1) // 2
        w = (W - 1) // 2
    
        with plt.xkcd():
            fig = plt.figure()
            ax = fig.add_subplot(111)
    
            vertices = []
            codes = []
    
            # loop over horizontals
            for r,rr in enumerate(xrange(1, H, 2)):
                run = []
                for c,cc in enumerate(xrange(1, W, 2)):
                    if grid[rr-1,cc]:
                        if not run:
                            run = [(r,c)]
                        run += [(r,c+1)]
                    elif run:
                        codes += [Path.MOVETO] + [Path.LINETO] * (len(run) - 1)
                        vertices += run
                        run = []
                if run:
                    codes += [Path.MOVETO] + [Path.LINETO] * (len(run) - 1)
                    vertices += run
    
            # grab bottom side of last row
            run = []
            for c,cc in enumerate(xrange(1, W, 2)):
                if grid[rr+1,cc]:
                    if not run:
                        run = [(r+1,c)]
                    run += [(r+1,c+1)]
                elif run:
                    codes += [Path.MOVETO] + [Path.LINETO] * (len(run) - 1)
                    vertices += run
                    run = []
                if run:
                    codes += [Path.MOVETO] + [Path.LINETO] * (len(run) - 1)
                    vertices += run
    
            # loop over verticles
            for c,cc in enumerate(xrange(1, W, 2)):
                run = []
                for r,rr in enumerate(xrange(1, H, 2)):
                    if grid[rr,cc-1]:
                        if not run:
                            run = [(r,c)]
                        run += [(r+1,c)]
                    elif run:
                        codes += [Path.MOVETO] + [Path.LINETO] * (len(run) - 1)
                        vertices += run
                        run = []
                        
                if run:
                    codes += [Path.MOVETO] + [Path.LINETO] * (len(run) - 1)
                    vertices += run
    
            # grab far right column
            run = []
            for r,rr in enumerate(xrange(1, H, 2)):
                if grid[rr,cc+1]:
                    if not run:
                        run = [(r,c+1)]
                    run += [(r+1,c+1)]
                elif run:
                    codes += [Path.MOVETO] + [Path.LINETO] * (len(run) - 1)
                    vertices += run
                    run = []
    
                if run:
                    codes += [Path.MOVETO] + [Path.LINETO] * (len(run) - 1)
                    vertices += run
    
            vertices = np.array(vertices, float)
            path = Path(vertices, codes)
    
            # for a line maze
            pathpatch = PathPatch(path, facecolor='None', edgecolor='black', lw=2)
            ax.add_patch(pathpatch)
    
            # hide axis and labels
            ax.axis('off')
            #ax.set_title('XKCD Maze')
            ax.dataLim.update_from_data_xy([(-0.1,-0.1), (h + 0.1, w + 0.1)])
            ax.autoscale_view()
    
            plt.show()
    
    plotXKCD(m.grid)

## Vocabulary

1. __biased__ - a maze is biased if the human eye can determine an obvious partial or complete solution very quickly
2. __cell__ - an open passage in the maze
3. __grid__ - the grid is the combination of all passages and barriers in the maze
4. __perfect__ - a maze is perfect if it has one and only one solution
5. __sparse__ - a sparse maze has walls or passages thicker than the usual single unit width
6. __wall__ - an impassable barrier in the maze
