
from mazelib.generate.MazeGenAlgo import np
from random import choice
# If the code is not Cython-compiled, we need to add some imports.
try:
    from cython import compiled
except ModuleNotFoundError:
    compiled = False
if not compiled:
    from mazelib.generate.MazeGenAlgo import MazeGenAlgo


class BinaryTree(MazeGenAlgo):
    """ TODO: describe algorithm
    """

    def __init__(self, w, h, skew=None):
        super(BinaryTree, self).__init__(w, h)
        skewes = {'NW': [(1, 0), (0, -1)],
                  'NE': [(1, 0), (0, 1)],
                  'SW': [(-1, 0), (0, -1)],
                  'SE': [(-1, 0), (0, 1)]}
        if skew in skewes:
            self.skew = skewes[skew]
        else:
            key = choice(list(skewes.keys()))
            self.skew = skewes[key]

    def generate(self):
        # create empty grid, with walls
        grid = np.empty((self.H, self.W), dtype=np.int8)
        grid.fill(1)

        for row in range(1, self.H, 2):
            for col in range(1, self.W, 2):
                grid[row][col] = 0
                neighbor_row, neighbor_col = self._find_neighbor(row, col)
                grid[neighbor_row][neighbor_col] = 0

        return grid

    def _find_neighbor(self, current_row, current_col):
        """ Find a neighbor in the skewed direction.
        """
        neighbors = []
        for b_row, b_col in self.skew:
            neighbor_row = current_row + b_row
            neighbor_col = current_col + b_col
            if neighbor_row > 0 and neighbor_row < (self.H - 1):
                if neighbor_col > 0 and neighbor_col < (self.W - 1):
                    neighbors.append((neighbor_row, neighbor_col))

        if len(neighbors) == 0:
            return (current_row, current_col)
        else:
            return choice(neighbors)
