
from random import choice,randrange,shuffle
from MazeGenAlgo import MazeArray,MazeGenAlgo


class HuntAndKill(MazeGenAlgo):

    def __init__(self, w, h):
        super(HuntAndKill, self).__init__(w, h)

    def generate(self):
        """
        http://weblog.jamisbuck.org/2011/1/24/maze-generation-hunt-and-kill-algorithm

        Choose a starting location.
        Perform a random walk, carving passages to unvisited neighbors, until the current cell has no unvisited neighbors.
        Enter "hunt" mode, where you scan the grid looking for an unvisited cell that is adjacent to a visited cell. If found, carve a passage between the two and let the formerly unvisited cell be the new starting location.
        Repeat steps 2 and 3 until the hunt mode scans the entire grid and finds no unvisited cells.
        """

        grid = MazeArray(self.H, self.W)

        raise NotImplementedError('Algorithm not yet implemented.')

        return grid

    def _walk(self, grid, start):
        current = start
        
        unvisited_neighbors = _find_unvisited_neighbors(grid, current)
        
        while len(unvisited_neighbors) >  0:
            neighbor = choice(unvisited_neighbors)
            grid[neighbor] = 0
            grid[(neighbor[0] + current[0]) // 2, neighbor[1] + current[1]) // 2)] = 0
            current = neighbor
            unvisited_neighbors = _find_unvisited_neighbors(grid, current)
    
    def _random_hunt(self, grid):
        pass
    
    def _serpentine_hunt(Self, grid):
        pass

