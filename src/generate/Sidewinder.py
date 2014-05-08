
from random import choice,random
from MazeGenAlgo import MazeArray,MazeGenAlgo


class Sidewinder(MazeGenAlgo):

    def __init__(self, h, w):
        super(Sidewinder, self).__init__(h, w)

    def generate(self):
        grid = MazeArray(self.H, self.W)

        # The first row is always empty, because you can't carve North
        for col in xrange(1, self.W - 1):
            grid[(1, col)] = 0

        # loop through the remaining rows and columns
        for row in xrange(3, self.H, 2):
            # create a run of cells
            run = []

            for col in xrange(1, self.W, 2):
                # remove the wall to the current cell
                grid[row, col] = 0
                # add the current cell to the run
                run.append((row, col))

                carve_east = random() > 0.5
                # carve East or North (can't carve East into the East wall
                if carve_east and col < (self.W - 2):
                    grid[row, col + 1] = 0
                else:
                    north = choice(run)
                    grid[north[0] - 1, north[1]] = 0
                    run = []

        return grid
