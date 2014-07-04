
from random import choice,shuffle
from MazeSolveAlgo import MazeSolveAlgo


class Tremaux(MazeSolveAlgo):
    """
    The Algorithm:

    1) create a solution for each starting position
     This Maze solving method is designed to be able to be used by a human inside of the Maze.
     It's similar to the recursive backtracker and will find a solution for all Mazes:
     As you walk down a passage, draw a line behind you to mark your path.
     When you hit a dead end turn around and go back the way you came.
     When you encounter a junction you haven't visited before, pick a new passage at random.
     If you're walking down a new passage and encounter a junction you have visited before,
     treat it like a dead end and go back the way you came.
     (That last step is the key which prevents you from going around in circles or missing passages in braid Mazes.)
     If walking down a passage you have visited before (i.e. marked once) and you encounter a junction,
     take any new passage if one is available, otherwise take an old passage
     (i.e. one you've marked once).
     All passages will either be empty, meaning you haven't visited it yet,
     marked once, meaning you've gone down it exactly once,
     or marked twice, meaning you've gone down it and were forced to backtrack in the opposite direction.
     When you finally reach the solution, paths marked exactly once will indicate a direct way back to the start.
     If the Maze has no solution, you'll find yourself back at the start with all passages marked twice. 

    Results

    Find one non-optimal solution. Works against imperfect mazes.
    """
    def _solve(self):
        raise Exception('This algorithm under development.')
        self.visited_coords = {}
        
        
        
        if len(solutions) == 0 or len(solutions[0]) == 0:
            raise ValueError('No valid solutions found.')

        return solutions

    def _visit(self, cell):
        """Increment the number of times a cell has been visited."""
        if cell not in self.visited_coords:
            self.visited_coords[cell] = 1
        else:
            self.visited_coords[cell] += 1

    def _get_visit_count(self, cell):
        """How many times has a cell been visited?"""
        if cell not in self.visited_coords:
            return 0
        else:
            return self.visited_coords[cell]
