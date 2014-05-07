
from random import choice,randrange,shuffle
from MazeGenAlgo import MazeGenAlgo
from MazeArray import MazeArray


class AldousBroder(MazeGenAlgo):

    def __init__(self, h, w):
        super(AldousBroder, self).__init__(h, w)

    def generate(self):
        grid = MazeArray(self.H, self.W)

        current = (randrange(1, self.H, 2), randrange(1, self.W, 2))
        grid[current] = 0
        num_visited = 1

        while num_visited < self.h * self.w:
            # find neighbors
            neighbors = self.find_neighors(current)

            # how many neighbors have already been visited?
            num_neighbors_not_visited = sum(map(lambda n: 1 if grid[n] else 0, neighbors))
            # if all of the neighbors have been visited:
            if num_neighbors_not_visited == 0:
                # mark random neighbor as current
                current = choice(neighbors)
                continue

            # loop through neighbors
            for neighbor in neighbors:
                # if neighbors has not been visited:
                if grid[neighbor]:
                    # open up wall to new neighbor
                    wall = ((neighbor[0]+current[0])/2, (neighbor[1]+current[1])/2)
                    grid[wall] = 0
                    # mark neighbor as visited
                    grid[neighbor] = 0
                    # bump the number visited
                    num_visited += 1
                    # current becomes new neighbor
                    current = neighbor
                    # break loop
                    break
    
        return grid
        
    def find_neighors(self, posi):
        (row, col) = posi
        ns = []

        if row > 1:
            ns.append((row-2, col))
        if row < self.H-2:
            ns.append((row+2, col))
        if col > 1:
            ns.append((row, col-2))
        if col < self.W-2:
            ns.append((row, col+2))

        shuffle(ns)

        return ns
