# Maze-Solving Algorithms

#####Go back to the main [README](../README.md)

## Blind Alley Filler
## Blind Alley Sealer
## Chain Algorithm
## Collision Solver
## Cul-de-sac Filler
## Dead End Filler
## Djikstra's
## Pledge Algorithm
## Random Mouse
## Recursive Backtracker
## Shortest Paths Finder
## Trémaux's Algorithm

## Wall Follower

###### The Algorithm

Ideally:

0. Follow the right wall and you will eventually end up at the end.

In reality:

1. Choose a random starting direction.
2. At each intersection, take the rightmost turn. At dead-ends, turn around.
3. If you have gone more than (H * W) + 2 cells, stop; the maze will not be solved.
4. Terminate when you reach the end cell.
5. Prune the extraneous branches from the solution before returning it.

###### Notes

To the human brain, this is the easiest possible way to solve a maze. Drunk college kids use this algorithm to solve corn mazes every year. But if we go purely by the number of lines of code, this is one of the hardest maze-solving algorithms to implement on a computer. Neat.

It should be noted that this algorithm does not solve mazes that are not perfect.


## Vocabulary

1. __biased__ - a maze is biased if there are long runs and corridors more in the North/South or East/West directions.
2. __cell__ - an open passage in the maze
3. __grid__ - the grid is the combination of all passages and barriers in the maze
4. __perfect__ - a maze is perfect if it has one and only one solution
5. __sparse__ - a sparse maze has walls or passages thicker than the usual single unit width
6. __wall__ - an impassable barrier in the maze


#####Go back to the main [README](../README.md)
