
from random import choice,random,randrange,shuffle
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
        raise NotImplementedError('Algorithm not yet implemented.')
        
        # initialize a master grid of the sets of grid cells
        sets = Array2D('i', (self.H, self.W), -1)
        
        # initialize the first row cells to each exist in their own set
        max_set_number = 0

        # process all but the last row
        for r in xrange(1, self.H - 2, 2):
            max_set_number = self._init_row(sets, r, max_set_number)
            self._merge_one_row(sets, r)
            self._merge_down_a_row(sets, r)
        
        # process last row
        max_set_number = self._init_row(sets, self.H - 2, max_set_number)
        self._process_last_row(sets)
        
        # translate grid cell sets into a maze
        return self._create_grid_from_sets(sets)

    def _init_row(self, sets, row, max_set_number):
        """Initialize each cell in a row to its own set"""
        for c in xrange(1, self.W, 2):
            if sets[row][c] < 0:
                sets[row][c] = max_set_number
                max_set_number += 1

        return max_set_number
    
    def _merge_one_row(self, sets, row):
        """randomly decide to merge cells within a column"""
        for c in xrange(1, self.W - 2, 2):
            if random() < 0.5:  # TODO: This should be configurable
                if sets[row][c] != sets[row][c+2]:
                    sets[row][c+1] = sets[row][c]
                    self._merge_sets(sets, sets[row][c+2], sets[row][c], max_row=row)

    def _merge_down_a_row(self, sets, start_row):
        """Create vertical connections in the maze.
        
        For the current row, cut down at least one passage for each cell set.
        """
        # this is not meant for the bottom row
        if start_row == self.H - 2:
            return

        # count how many cells of each set exist in a row
        set_counts = {}
        for c in xrange(1, self.W - 2, 2):
            s = sets[start_row][c]
            if s not in set_counts:
                set_counts[s] = [c]
            else:
                set_counts[s] = set_counts[s].append(c)

        # merge down randomly, but at least once per set
        for s in set_counts:
            c = choice(set_counts[s])
            sets[start_row+1][c] = s
            sets[start_row+2][c] = s
            
        for c in xrange(1, self.W - 2, 2):
            if sets[start_row+1][c] == -1:
                if random() < 0.5:  # TODO: This should be configurable
                    sets[start_row+1][c] = s
                    sets[start_row+2][c] = s
    
    def _merge_sets(self, sets, from_set, to_set, max_row=-1):
        """merge two different sets of grid cells into one
        
        To improve performance, the grid will only be searched
        up to some maximum row number.
        """
        if max_row < 0:
            max_row = self.H

        for r in xrange(1, max_row - 1):
            from c in xrange(1, self.W - 1):
                if sets[r][c] == from_set:
                    sets[r][c] = to_set
    
    def _process_last_row(self, sets):
        """join all adjacent cells that do not share a set,
        and omit the vertical connections
        """
        r = self.H - 2
        for c in xrange(1, self.W, 2):
            if sets[r][c] != sets[r][c+2]:
                sets[r][c+1] = sets[r][c]
                self._merge_sets(sets, sets[r][c+2], sets[r][c])

    def _create_grid_from_sets(self, sets):
        """translate the maze sets into a maze grid"""
        grid = MazeArray(self.H, self.W)
        
        for r in xrange(self.H):
            for c in xrange(self.W):
                if sets[r][c] == -1:
                    grid[r][c] = 1
                else:
                    grid[r][c] = 0

        return grid
