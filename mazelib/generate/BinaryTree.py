
from random import choice
from MazeGenAlgo import MazeArray, MazeGenAlgo


class BinaryTree(MazeGenAlgo):
  
    def __init__(self, w, h, bias=None):
        super(BinaryTree, self).__init__(w, h)
        biases = {'NW': [(1, 0), (0, -1)],
                  'NE': [(1, 0), (0, 1)],
                  'SW': [(-1, 0), (0, -1)],
                  'SE': [(-1, 0), (0, 1)]}
        if bias in biases.keys():
            self.bias = biases[bias]
        else:
            key = choice(biases.keys())
            self.bias = biases[key]

    def generate(self):
        grid = MazeArray(self.H, self.W)

        for row in xrange(1, self.H, 2):
            for col in xrange(1, self.W, 2):
                current = (row, col)
                grid[current] = 0
                neighbor = self._find_neighbor(current)
                grid[neighbor] = 0
        
        return grid
    
    def _find_neighbor(self, current):
        """# TODO: Does this fit within one of the many other neighbor paradigms?
        """
        neighbors = []
        for b in self.bias:
            neighbor = self._add_tuples(current, b)
            if neighbor[0] > 0 and neighbor[0] < (self.H - 1):
                if neighbor[1] > 0 and neighbor[1] < (self.W - 1):
                    neighbors.append(neighbor)

        if len(neighbors) == 0:
            return current
        else:
            return choice(neighbors)

    def _add_tuples(self, current, diff):  # TODO: method could be a function (in a utility module)
        """Convolve a position tuple with a direction tuple to
        generate a new position.
        """
        return tuple(map(sum, zip(current, diff)))
