
from random import choice,randrange
from MazeGenAlgo import MazeArray,MazeGenAlgo


class CellularAutomaton(MazeGenAlgo):
    
    # TODO: These mazes seem flawed for when small, the outer walls are too open.
  
    def __init__(self, w, h, complexity=1.0, density=1.0):
        super(CellularAutomaton, self).__init__(w, h)
        self.complexity = complexity
        self.density = density

    def generate(self):
        """Generate a new maze using a cellular automaton algorithm"""
        # Adjust complexity and density relative to maze size
        self.complexity = int(self.complexity * (5 * (self.H + self.W)))
        self.density    = int(self.density * (self.h * self.w))

        # Build actual maze
        grid = MazeArray(self.H, self.W, 0)
        # Fill borders
        grid[0, :] = grid[-1, :] = 1
        grid[:, 0] = grid[:, -1] = 1

        # Make isles
        for i in xrange(self.density):
            y, x = randrange(0, self.H, 2), randrange(0, self.W, 2)
            grid[y, x] = 1
            for j in xrange(self.complexity):
                neighbours = []
                if x > 1:           neighbours.append((y, x - 2))
                if x < self.W - 2:  neighbours.append((y, x + 2))
                if y > 1:           neighbours.append((y - 2, x))
                if y < self.H - 2:  neighbours.append((y + 2, x))
                if len(neighbours):
                    y_,x_ = choice(neighbours)
                    if grid[y_, x_] == 0:
                        grid[y_, x_] = 1
                        grid[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                        x, y = x_, y_

        return grid
