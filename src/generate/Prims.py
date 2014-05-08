
from random import randrange,shuffle
from MazeGenAlgo import MazeGenAlgo,MazeArray


class Prims(MazeGenAlgo):

    def __init__(self, h, w):
        super(Prims, self).__init__(h, w)

    def generate(self):
        grid = MazeArray(self.H, self.W)

        # choose a random starting position
        current = (randrange(1, self.H, 2), randrange(1, self.W, 2))
        grid[current] = 0

        # created a weighted list of all vertices connected in the graph
        neighbors = self._find_neighbors(grid, current, False)

        # loop over all current neighbors, until empty
        visited = 1

        while visited < self.h * self.w:
            # find neighbor with lowest weight, make it current
            nn = randrange(len(neighbors))
            current = neighbors[nn]
            visited += 1
            grid[current] = 0
            neighbors = neighbors[:nn] + neighbors[nn + 1:]
            # connect that neighbor to a random neighbor with grid[posi] == 0
            nearest_n = self._find_neighbors(grid, current, True)[0]
            grid[(current[0] + nearest_n[0]) // 2, (current[1] + nearest_n[1]) // 2] = 0

            # find all unvisited neighbors of current, add them to neighbors
            unvisited = self._find_neighbors(grid, current, False)
            for unv in unvisited:
                if unv not in neighbors:
                    neighbors.append(unv)

        return grid

    def _find_neighbors(self, grid, current, visited):
        row,col = current
        ns = []

        flag = 0 if visited else 1

        if row > 1 and grid[(row - 2, col)] == flag:
            ns.append((row - 2, col))
        if row < self.H - 2 and grid[(row + 2, col)] == flag:
            ns.append((row + 2, col))
        if col > 1 and grid[(row, col - 2)] == flag:
            ns.append((row, col - 2))
        if col < self.W - 2 and grid[(row, col + 2)] == flag:
            ns.append((row, col + 2))

        shuffle(ns)

        return ns
