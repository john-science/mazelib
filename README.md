# mazelib

#### A Python API for creating and solving mazes.  --  WORK IN PROGRESS

## The mazelib API

The mazelib library supports Python versions 2.6.x, 2.7.x, and 3.x.

### Generating Mazes

    from mazelib import *

    m = Maze()
    m.generator = Prims()
    m.generate(27, 34)

### Solving Mazes

    m.solver = WallFollower()
    m.generate_entrances()
    m.solve()

## The Algorithms

There are many algorithms for generating and solving mazes. And the implementation in this library have many optional parameters. To learn more, look in the documentation:

#### [Maze-Generating Algorithms](MAZE_GEN_ALGOS.md)

#### [Maze-Solving Algorithms](MAZE_SOLVE_ALGOS.md)


## Using the Results

For the rest of this section, let us assume we have already generated a maze:

    from mazelib import *

    m = Maze()
    m.generator = Prims()
    m.generate(27, 34)

#### Example 1: Plotting the Maze in Plain Text

It is helpful to have a low-key, fast way to print out mazes (and solutions) as you develop. The library itself actually has a built-in tostring method:

    print(m.grid.tostring())            # print walls only
    print(m.grid.tostring(True))        # print walls and entrances
    print(m.grid.tostring(True, True))  # print walls, entrances, and solution
    print(str(m.grid))                  # print everything that is available

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

1. __biased__ - a maze is biased if there are long runs and corridors more in the North/South or East/West directions.
2. __cell__ - an open passage in the maze
3. __grid__ - the grid is the combination of all passages and barriers in the maze
4. __perfect__ - a maze is perfect if it has one and only one solution
5. __sparse__ - a sparse maze has walls or passages thicker than the usual single unit width
6. __wall__ - an impassable barrier in the maze
