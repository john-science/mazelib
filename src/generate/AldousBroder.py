
from random import choice,randrange,shuffle
from MazeGenAlgo import MazeArray,MazeGenAlgo


class AldousBroder(MazeGenAlgo):
    """ 
    1. Choose a random cell.
    2. Choose a random neighbor of the current cell and visit it. If the neighbor has not
        yet been visited, add the traveled edge to the spanning tree.
    3. Repeat step 2 until all cells have been visited.
    """

    def __init__(self, h, w):
        super(AldousBroder, self).__init__(h, w)

    def generate(self):
        grid = MazeArray(self.H, self.W)
        
        current = (randrange(1, self.H, 2), randrange(1, self.W, 2))
        grid[current] = 0
        num_visited = 1

        while num_visited < self.h * self.w:
            # find neighbors
            neighbors = self._find_neighors(current, grid)

            # how many neighbors have already been visited?
            if len(neighbors) == 0:
                # mark random neighbor as current
                current = choice(self._find_neighors(current, grid, False))
                continue

            # loop through neighbors
            for neighbor in neighbors:
                if grid[neighbor]:
                    # open up wall to new neighbor
                    grid[((neighbor[0]+current[0])//2, (neighbor[1]+current[1])//2)] = 0
                    # mark neighbor as visited
                    grid[neighbor] = 0
                    # bump the number visited
                    num_visited += 1
                    # current becomes new neighbor
                    current = neighbor
                    # break loop
                    break
    
        return grid

    # TODO: Several algorithms use this method, should they share it?
    def _find_neighors(self, posi, grid, visited=True):
        """ Find all the neighbors in the grid of the current position,
        that have/haven't been visited.
        """
        (row, col) = posi
        ns = []

        if row > 1 and grid[row-2, col] == visited:
            ns.append((row-2, col))
        if row < self.H-2 and grid[row+2, col] == visited:
            ns.append((row+2, col))
        if col > 1 and grid[row, col-2] == visited:
            ns.append((row, col-2))
        if col < self.W-2 and grid[row, col+2] == visited:
            ns.append((row, col+2))

        shuffle(ns)

        return ns

