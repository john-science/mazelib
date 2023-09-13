# mazelib Examples

##### Go back to the main [README](../README.md)


## Generating Special Mazes

#### Dungeons, sans Dragons

When creating mazes for use in games you will frequently want to have big, empty rooms included within the maze. The DungeonRooms algorithm was included for just this purpose. It is a simple variation on the classic Hunt-and-Kill algorithm, but it accepts information about open rooms you want included in the maze.

To open up rooms in a maze, DungeonRooms accepts two optional input parameters:

* rooms: List(List(tuple, tuple))
 * A list of lists, containing the top-left and bottom-right corners of the rooms you want to create. For best results, the corners of each room shouldhave odd-numbered coordinates.
* grid: 2D NumPy array, of booleans, all set to `True`
 * A pre-built maze array filled with one, or many, rooms.

Let's do an example of each method for defining input rooms:

##### Defining Room Corners

Here we create a 24x33 maze with one rectangular 4x4 room, open between the corners (3, 3) and (7, 7):

    from mazelib.generate.DungeonRooms import DungeonRooms

    m = Maze()
    m.generator = DungeonRooms(24, 33, rooms=[[(3,3), (7,7)]])
    m.generate()

##### Defining Rooms by an Input Grid

Here we create a 4x4 maze with one rectangular 2x2 room, open between the corners (5, 5) and (7, 7):

    import numpy as np
    g = np.ones((9, 9), dtype=np.int8)
    g[5] = np.array([1,1,1,0,0,0,1])
    a[6] = np.array([1,1,1,0,0,0,1])
    g[7] = np.array([1,1,1,0,0,0,1])

    m = Maze()
    m.generator = DungeonRooms(4, 4, grid=g)
    m.generate()

![Dungeon Rooms Example](images/dungeon_rooms_4x4_plain.png?raw=true)


#### Transmuting Attractive Mazes

Perhaps you want more control over your maze. You have ideas in you imagine spiral mazes, or circular mazes with a room at the very center. The Perturbation algorithm will allow you to do all of these things.

First, start with a simple spiral maze (which is trivial to solve):

    import numpy as np
    g = np.ones((11, 11), dtype=np.int8)
    g[1] = np.array([1,0,0,0,0,0,0,0,0,0,1])
    g[2] = np.array([1,1,1,1,1,1,1,1,1,0,1])
    g[3] = np.array([1,0,0,0,0,0,0,0,1,0,1])
    g[4] = np.array([1,0,1,1,1,1,1,0,1,0,1])
    g[5] = np.array([1,0,1,0,0,0,1,0,1,0,1])
    g[6] = np.array([1,0,1,0,1,1,1,0,1,0,1])
    g[7] = np.array([1,0,1,0,0,0,0,0,1,0,1])
    g[8] = np.array([1,0,1,1,1,1,1,1,1,0,1])
    g[9] = np.array([1,0,0,0,0,0,0,0,0,0,1])

![sprial maze](images/spiral_1.png?raw=true)

    from mazelib.generate.Prims import Prims
    from mazelib.transmute.Perturbation import Perturbation

    m = Maze()
    m.generator = Prims(5, 5)
    m.generate()
    m.grid = g  # for a good example
    m.transmuters = [Perturbation(repeat=1, new_walls=3)]
    m.transmute()
    m.start = (1, 0)
    m.end = (5, 5)

The end result is a maze that is *almost* a spiral, but enough different to still make a decent maze.

![perturbated sprial maze](images/perturbation_1.png?raw=true)

## Displaying a Maze

For the rest of this section, let us assume we have already generated a maze:

    from mazelib import Maze
    from mazelib.generate.Prims import Prims

    m = Maze()
    m.generator = Prims(27, 34)
    m.generate()

#### Example 1: Plotting the Maze in Plain Text

If you want a low-key, fast way to view the maze you've generated, just use the library's built-in `tostring` method:

    print(m.tostring())            # print walls only
    print(m.tostring(True))        # print walls and entrances
    print(m.tostring(True, True))  # print walls, entrances, and solution
    print(str(m))                  # print everything that is available
    print(m)                       # print everything that is available

The above `print` calls would generate these types of plots, respectively:

    ###########         ###########         ###########
    # #   #   #         S #   #   #         S*#   #   #
    # ### # # #         # ### # # #         #*### # # #
    # #     # #         # #     # #         #*#     # #
    # ### #####         # ### #####         #*### #####
    #         #         #         #         #***      #
    ### #######         ### #######         ###*#######
    #         E         #         E         #  *******E
    ###########         ###########         ###########


#### Example 2: Plotting the Maze with Matplotlib

Sometimes it is hard to see the finer points of a maze in plain text. You may want to see at a glance if the maze has unreachable sections, if it has loops or free walls, if it is obviously too easy, etcetera.

    import matplotlib.pyplot as plt

    def showPNG(grid):
        """Generate a simple image of the maze."""
        plt.figure(figsize=(10, 5))
        plt.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
        plt.xticks([]), plt.yticks([])
        plt.show()

![Prims Example](images/prims_5x5_plain.png?raw=true)


#### Example 3: Displaying the Maze as CSS

CSS and HTML are universal and easy to use. Here is a simple (if illegible) example to display your maze in CSS and HTML:

    def toHTML(grid, start, end, cell_size=10):
        row_max = grid.shape[0]
        col_max = grid.shape[1]

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
               'div.maze_row div.rd{background-color: red;}' + \
               'div.maze_row div.gr{background-color: green;}' + \
               'div.maze_row div{float: left;}' + \
               'div.maze_row:after{content: ".";height: 0;visibility: hidden;display: block;clear: both;}' + \
               '</style></head><body>' + \
               '<div id="maze">'

        for row in range(row_max):
            html += '<div class="maze_row">'
            for col in range(col_max):
                if (row, col) == start:
                    html += '<div class="gr"></div>'
                elif (row, col) == end:
                    html += '<div class="rd"></div>'
                elif grid[row][col]:
                    html += '<div class="bl"></div>'
                else:
                    html += '<div class="wh"></div>'
            html += '</div>'
        html += '</div></body></html>'

        return html

![CSS/HTML Example](images/css_4x5.png?raw=true)


#### Example 4: Drawing the Maze with XKCD style

Chances are, if you're reading this you probably like XKCD. So, let's make the maze look like Randal drew it.

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
            for r,rr in enumerate(range(1, H, 2)):
                run = []
                for c,cc in enumerate(range(1, W, 2)):
                    if grid[rr-1,cc]:
                        if not run:
                            run = [(r,c)]
                        run += [(r,c+1)]
                    else:
                        use_run(codes, vertices, run)
                        run = []
                use_run(codes, vertices, run)

            # grab bottom side of last row
            run = []
            for c,cc in enumerate(range(1, W, 2)):
                if grid[H-1,cc]:
                    if not run:
                        run = [(H//2,c)]
                    run += [(H//2,c+1)]
                else:
                    use_run(codes, vertices, run)
                    run = []
                use_run(codes, vertices, run)

            # loop over verticles
            for c,cc in enumerate(range(1, W, 2)):
                run = []
                for r,rr in enumerate(range(1, H, 2)):
                    if grid[rr,cc-1]:
                        if not run:
                            run = [(r,c)]
                        run += [(r+1,c)]
                    else:
                        use_run(codes, vertices, run)
                        run = []
                use_run(codes, vertices, run)

            # grab far right column
            run = []
            for r,rr in enumerate(range(1, H, 2)):
                if grid[rr,W-1]:
                    if not run:
                        run = [(r,W//2)]
                    run += [(r+1,W//2)]
                else:
                    use_run(codes, vertices, run)
                    run = []
                use_run(codes, vertices, run)

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

    def use_run(codes, vertices, run):
        """Helper method for plotXKCD. Updates path with newest run."""
        if run:
            codes += [Path.MOVETO] + [Path.LINETO] * (len(run) - 1)
            vertices += run

    plotXKCD(m.grid)

![XKCD Example](images/xkcd_5x6.png?raw=true)


##### Go back to the main [README](../README.md)
