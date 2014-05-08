
from random import randrange,shuffle
from MazeGenAlgo import MazeGenAlgo


class Wilsons(MazeGenAlgo):

    def __init__(self, w, h):
        super(Wilsons, self).__init__(w, h)

    def generate(self):
        """
        http://weblog.jamisbuck.org/2011/1/20/maze-generation-wilson-s-algorithm

        Choose any vertex at random and add it to the UST.
        Select any vertex that is not already in the UST and perform a random walk until you encounter a vertex that is in the UST.
        Add the vertices and edges touched in the random walk to the UST.
        Repeat 2 and 3 until all vertices have been added to the UST.
        """

        grid = MazeArray(self.H, self.W)

        raise NotImplementedError('Algorithm not yet implemented.')

        return grid
