
import abc
from random import choice,random,randrange,shuffle
import sys


class Maze(object):

    def __init__(self):
        # TODO: Consider allowing these passed as optional parameters to Maze.
        self.generator = None
        self.grid = None
        self.solver = None
        self.solution = None
        self.start = None
        self.end = None

    def generate(self):
        self.grid = self.generator.generate()

    def generate_random_entrances(self):
        rows = len(self.grid)
        cols = len(self.grid[0])

        start_side = randrange(4)

        if start_side == 0:
            self.start = (0, randrange(1, cols, 2))         # North
            self.end = (rows - 1, randrange(1, cols, 2))
        elif start_side == 1:
            self.start = (rows - 1, randrange(1, cols, 2))  # South
            self.end = (0, randrange(1, cols, 2))
        elif start_side == 2:
            self.start = (randrange(1, rows, 2), 0)          # West
            self.end = (randrange(1, rows, 2), cols - 1)
        else:
            self.start = (randrange(1, rows, 2), cols - 1)   # East
            self.end = (randrange(1, rows, 2), 0)

    def solve(self):
        raise NotImplementedError('Please Implement this method.')

    def tostring(self, focus='passages'):
        """Return a string representation of the maze."""
        if focus == 'walls':
            return self._walls_string()
        else:
            return self._passages_string()

    def _passages_string(self):
        """Return a string representation of the maze."""
        txt = ''
        for row in self.grid:
            for cell in row:
                txt += '#' if cell else ' '
            txt += '\n'

        return txt

    def _walls_string(self):
        """Return a string representation of the maze."""
        row_max = len(self.grid)
        col_max = len(self.grid[0])
        
        def find_num_connected_walls(row, col):
            num = 0
            if col > 0 and self.grid[row][col-1]:
                num += 1
            if col < (col_max -1) and self.grid[row][col+1]:
                num += 1
            if row > 0 and self.walls[row-1][col]:
                num += 1
            if row < (row_max - 1) and self.grid[row+1][col]:
                num += 1
            
            return num
        
        txt = ''
        for row in xrange(row_max):
            for col in xrange(col_max):
                if not self.grid[row][col]:
                    txt += ' '
                else:
                    number_of_connected_walls = find_num_connected_walls(row, col)
                    if number_of_connected_walls != 2:
                        txt += '+'
                    elif row > 0 and row < (row_max - 1) and self.grid[row-1][col] and self.grid[row+1][col]:
                        txt += '|'
                    elif col > 0 and col < (col_max - 1) and self.grid[row][col-1] and self.grid[row][col+1]:
                        txt += '-'
                    else:
                        txt += '+'
            txt += '\n'

        return txt

    def __str__(self):
        # TODO: Should Maze be represented by the maze, and not the other class info?
        self._to_dense_string()

    def __repr__(self):
        return self.__str__()
    
    def toHTML(self, cell_size=10):
        row_max = len(self.grid)
        col_max = len(self.grid[0])
        
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
                if self.walls[row][col]:
                    html += '<div class="bl"></div>'
                else:
                    html += '<div class="wh"></div>'
            html += '</div>'
        
        html += '</div></body></html>'
        
        return html
