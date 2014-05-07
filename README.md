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

    def showPNG(walls_array):
        """Generate a simple image of the maze."""
        walls = []
        for wall in walls_array:
            walls.append(list(wall))
    
        plt.figure(figsize=(10, 5))
        plt.imshow(walls, cmap=plt.cm.binary, interpolation='nearest')
        plt.xticks([]), plt.yticks([])
        plt.show()

#### Example 3: Displaying the Maze as CSS

Just a simple function to draw a maze in CSS/HTML. The benefit here is you don't need any special Python libraries. And CSS is really easy to fine-tune to customize the final output.

    def toHTML(grid, cell_size=10):
        row_max = len(grid)
        col_max = len(grid[0])
        
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

    def plotXKCD(grid):
        """ Generate an XKCD-styled line-drawn image of the maze. """
        H = walls_array.height
        W = grid.width
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
                    if grid[(rr-1,cc)]:
                        if run:
                            run += [(r,c+1)]
                        else:
                            run = [(r,c), (r,c+1)]
                    else:
                        if run:
                            codes += [Path.MOVETO] + [Path.LINETO] * (len(run) - 1)
                            vertices += run
                        run = []
                if run:
                    codes += [Path.MOVETO] + [Path.LINETO] * (len(run) - 1)
                    vertices += run
            
            # grab bottom side of last row
            run = []
            for c,cc in enumerate(xrange(1, W, 2)):
                if grid[(rr+1,cc)]:
                    if run:
                        run += [(r+1,c+1)]
                    else:
                        run = [(r+1,c), (r+1,c+1)]
                else:
                    if run:
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
                    if grid[(rr,cc-1)]:
                        if run:
                            run += [(r+1,c)]
                        else:
                            run = [(r,c), (r+1,c)]
                    else:
                        if run:
                            codes += [Path.MOVETO] + [Path.LINETO] * (len(run) - 1)
                            vertices += run
                        run = []
                if run:
                    codes += [Path.MOVETO] + [Path.LINETO] * (len(run) - 1)
                    vertices += run
                        
            # grab far right column
            run = []
            for r,rr in enumerate(xrange(1, H, 2)):
                if grid[(rr,cc+1)]:
                    if run:
                        run += [(r+1,c+1)]
                    else:
                        run = [(r,c+1), (r+1,c+1)]
                else:
                    if run:
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


## Vocabulary

1. __biased__ - a maze is biased if the human eye can determine an obvious partial or complete solution very quickly
2. __cell__ - an open passage in the maze
3. __grid__ - the grid is the combination of all passages and barriers in the maze
4. __perfect__ - a maze is perfect if it has one and only one solution
5. __wall__ - an impassable barrier in the maze
