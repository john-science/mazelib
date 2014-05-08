
from random import randrange,shuffle
from MazeGenAlgo import MazeGenAlgo
from MazeArray import MazeArray


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
            connections, and you're done!
        """

        grid = MazeArray(self.H, self.W)

        raise NotImplementedError('Algorithm not yet implemented.')

        return grid
