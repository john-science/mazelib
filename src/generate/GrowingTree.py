
from random import choice,random,randrange,shuffle
from MazeGenAlgo import MazeArray,MazeGenAlgo


class GrowingTree(MazeGenAlgo):
    """
    The Algorithm
    
    1. Let C be a list of cells, initially empty. Add one cell to C, at random.
    2. Choose a cell from C, and carve a passage to any unvisited neighbor of that cell,
        adding that neighbor to C as well. If there are no unvisited neighbors,
        remove the cell from C.
    3. Repeat step 2 until C is empty.
    
    Optional Parameters
    
    backtrack_chance: Float [0.0, 1.0]
        Splits the logic to either use Recursive Backtracking (RB) or Prim's (random)
        to select the next cell to visit. (default 1.0)
    """
  
    def __init__(self, w, h, backtrack_chance=1.0):
        super(GrowingTree, self).__init__(w, h)
        self.backtrack_chance = backtrack_chance

    def generate(self):
        grid = MazeArray(self.H, self.W)

        current = (randrange(1, self.H, 2), randrange(1, self.W, 2))
        grid[current] = 0
        active = self.find_neighbors(current, grid, True)
        active = [current]

        # continue until you have no more neighbors to move to
        while active:
            if random() < self.backtrack_chance:
                current = active[-1]
            else:
                current = choice(active)

            # find a visited neighbor
            next_neighbors = self.find_neighbors(current, grid, True)
            if len(next_neighbors) == 0:
                active = [a for a in active if a != current]
                continue

            nn = choice(next_neighbors)
            active += [nn]

            grid[nn] = 0
            grid[(current[0] + nn[0]) // 2, (current[1] + nn[1]) // 2] = 0

        return grid
