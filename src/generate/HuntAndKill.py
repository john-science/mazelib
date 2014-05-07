
from random import randrange,shuffle
from MazeGenAlgo import MazeGenAlgo
from MazeArray import MazeArray


class HuntAndKill(MazeGenAlgo):

    def __init__(self, w, h):
        super(HuntAndKill, self).__init__(w, h)

    def generate(self):
        """
        http://weblog.jamisbuck.org/2011/1/24/maze-generation-hunt-and-kill-algorithm

        Choose a starting location.
        Perform a random walk, carving passages to unvisited neighbors, until the current cell has no unvisited neighbors.
        Enter “hunt” mode, where you scan the grid looking for an unvisited cell that is adjacent to a visited cell. If found, carve a passage between the two and let the formerly unvisited cell be the new starting location.
        Repeat steps 2 and 3 until the hunt mode scans the entire grid and finds no unvisited cells.
        """

        grid = MazeArray(self.H, self.W)

        raise NotImplementedError('Algorithm not yet implemented.')

        return grid
