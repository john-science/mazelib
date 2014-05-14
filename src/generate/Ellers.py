
from random import randrange,shuffle
from MazeGenAlgo import MazeGenAlgo,MazeArray
from ..utils.array2d import Array2D


class Ellers(MazeGenAlgo):

    def __init__(self, w, h):
        super(Ellers, self).__init__(w, h)

    def generate(self):
        """
        http://weblog.jamisbuck.org/2010/12/29/maze-generation-eller-s-algorithm
        
        Initialize the cells of the first row to each exist in their own set.
        Now, randomly join adjacent cells, but only if they are not in the same set. When joining
            adjacent cells, merge the cells of both sets into a single set, indicating that all
            cells in both sets are now connected (there is a path that connects any two cells in
            the set).
        For each set, randomly create vertical connections downward to the next row. Each remaining
            set must have at least one vertical connection. The cells in the next row thus connected
            must share the set of the cell above them.
        Flesh out the next row by putting any remaining cells into their own sets.
        Repeat until the last row is reached.
        For the last row, join all adjacent cells that do not share a set, and omit the vertical
            connections.
        """

        if self.H < 3:
            raise ValueError('Ellers Algorithm requires at least three rows.')

        grid = MazeArray(self.H, self.W)

        raise NotImplementedError('Algorithm not yet implemented.')
        
        # initialize a master grid of the sets of grid cells
        sets = Array2D('i', (self.H, self.W), -1)
        
        # initialize the first row cells to each exist in their own set
        max_set_number = 0
        for c in xrange(1, self.W, 2):
            sets[0][c] = max_set_number
            max_set_number += 1

        # process all but first and last rows
        
        # process last row
        

        return grid
    
    def _merge_sets(self, sets, from_set, to_set, max_row=-1):
        """merge two different sets of grid cells into one
        
        To improve performance, the grid will only be searched
        up to some maximum row number.
        """
        if max_row < 0:
            max_row = self.H

        for r in xrange(1, max_row, 2):
            from c in xrange(1, self.W, 2):
                if sets[r][c] == from_set:
                    sets[r][c] = to_set

