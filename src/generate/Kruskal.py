
from random import shuffle
from MazeGenAlgo import MazeGenAlgo
from MazeArray import MazeArray


class Kruskal(MazeGenAlgo):
  
    def __init__(self, h, w):
        super(Kruskal, self).__init__(h, w)

    def generate(self):
        grid = MazeArray(self.H, self.W)

        forest = []
        for row in xrange(1, self.H - 1, 2):
            for col in xrange(1, self.W -1, 2):
                forest.append([(row, col)])
                grid[row, col] = 0

        edges = []
        for row in xrange(2,self.H - 1,2):
            for col in xrange(1,self.W - 1,2):
                edges.append((row,col))
        for row in xrange(1,self.H - 1,2):
            for col in xrange(2,self.W - 1,2):
                edges.append((row,col))

        shuffle(edges)

        while len(forest) > 1:
            ce = edges[0]
            edges = edges[1:]
           
            tree1 = -1
            tree2 = -1
            
            if ce[0]%2 == 0:  # even-numbered row: vertical wall
                tree1 = sum([i if (ce[0]-1, ce[1]) in j else 0 for i,j in enumerate(forest)])
                tree2 = sum([i if (ce[0]+1, ce[1]) in j else 0 for i,j in enumerate(forest)])
            else:  # odd-numbered row: horizontal wall
                tree1 = sum([i if (ce[0], ce[1]-1) in j else 0 for i,j in enumerate(forest)])
                tree2 = sum([i if (ce[0], ce[1]+1) in j else 0 for i,j in enumerate(forest)])
           
            if tree1 != tree2:
                new_tree = forest[tree1] + forest[tree2]
                temp1 = list(forest[tree1])
                temp2 = list(forest[tree2])
                forest = [x for x in forest if x != temp1]  # faster than forest.remove(temp1)
                forest = [x for x in forest if x != temp2]
                forest.append(new_tree)
                grid[ce] = 0

        return grid
