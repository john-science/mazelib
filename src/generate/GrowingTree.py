
from random import choice,random,randrange,shuffle
from MazeGenAlgo import MazeGenAlgo
from MazeArray import MazeArray


class GrowingTree(MazeGenAlgo):
    """
    The input optional extra input parameter 'backtrack_chance'
    splits the logic to either use Recursive Backtracking (RB)
    or Prim's (random) to select the next cell to visit.

    a value of 1.0 will mean you always use RB
    a value of 0.0 will mean you always use Prim's
    """
  
    def __init__(self, w, h, backtrack_chance=1.0):
        super(GrowingTree, self).__init__(w, h)
        self.backtrack_chance = backtrack_chance

    def generate(self):
        grid = MazeArray(self.H, self.W)

        current = (randrange(1, self.H, 2), randrange(1, self.W, 2))
        grid[current] = 0
        active = self._find_unvisited_neighbors(current, grid)
        active = [current]

        while active:
            if random() < self.backtrack_chance:
                current = active[-1]
            else:
                current = choice(active)

            next_neighbors = self._find_unvisited_neighbors(current, grid)
            if len(next_neighbors) == 0:
                active = [a for a in active if a != current]
                continue

            nn = choice(next_neighbors)
            active += [nn]

            grid[nn] = 0
            grid[(current[0] + nn[0]) // 2, (current[1] + nn[1]) // 2] = 0

        return grid

    def _find_unvisited_neighbors(self, current, grid):
        neighbors = []

        row,col = current
        if row > 1 and grid[row - 2, col] == 1:
            neighbors.append((row - 2, col))
        if row < (self.H - 2) and grid[row + 2, col] == 1:
            neighbors.append((row + 2, col))
        if col > 1 and grid[row, col - 2] == 1:
            neighbors.append((row, col - 2))
        if col < (self.W - 2) and grid[row, col + 2] == 1:
            neighbors.append((row, col + 2))

        shuffle(neighbors)
        return neighbors

    def _find_visited_neighbors(self, current, grid):
        neighbors = []

        row,col = current
        if row > 1 and grid[row - 2, col] == 0:
            neighbors.append((row - 2, col))
        if row < (self.H - 2) and grid[row + 2, col] == 0:
            neighbors.append((row + 2, col))
        if col > 1 and grid[row, col - 2] == 0:
            neighbors.append((row, col - 2))
        if col < (self.W - 2) and grid[row, col + 2] == 0:
            neighbors.append((row, col + 2))

        shuffle(neighbors)
        return neighbors


