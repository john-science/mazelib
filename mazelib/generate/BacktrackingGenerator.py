
from random import randrange,shuffle
from MazeGenAlgo import MazeArray,MazeGenAlgo


class BacktrackingGenerator(MazeGenAlgo):
    """
    1. Randomly choose a starting cell.
    2. Randomly choose a wall at the current cell and open a passage through to any random adjacent
        cell, that has not been visited yet. This is now the current cell.
    3. If all adjacent cells have been visited, back up to the previous and repeat step 2.
    4. Stop when the algorithm has backed all the way up to the starting cell.
    """

    def __init__(self, w, h):
        super(BacktrackingGenerator, self).__init__(w, h)

    def generate(self):
        grid = MazeArray(self.H, self.W)

        current = (randrange(1, self.H, 2), randrange(1, self.W, 2))
        track = [current]
        grid[current] = 0

        while track:
            current = track[-1]
            neighbors = self.find_neighbors(current, grid, True)

            if len(neighbors) == 0:
                track = track[:-1]
            else:
                nn = neighbors[0]
                grid[nn] = 0
                grid[(nn[0] + current[0]) // 2, (nn[1] + current[1]) // 2] = 0

                track += [nn]

        return grid
