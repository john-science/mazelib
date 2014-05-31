# Maze-Solving Algorithms

#####Go back to the main [README](../README.md)

## Blind Alley Filler
## Blind Alley Sealer
## Chain Algorithm
## Collision Solver
## Cul-de-sac Filler
## Dead End Filler

###### The Algorithm

Just scan the Maze, and fill in each dead end, filling in the
passage backwards from the block until you reach a junction. This
includes filling in passages that become parts of dead ends once
other dead ends are removed. At the end only the solution will
remain, or solutions if there are more than one.

What is left is a maze with only solution tiles. Loop through
these cells with shortest paths to find all solutions.

###### Results

###### Notes

This is a simple Maze solving algorithm.
It focuses on the Maze, is always very fast, and uses no extra
memory.

This will always find the one unique solution for perfect Mazes,
but won't do much in heavily braid Mazes, and in fact won't do
anything useful at all for those Mazes without dead ends.

## Djikstra's
## Pledge Algorithm
## Random Mouse
## Recursive Backtracker
## Shortest Path Finder

###### The Algorithm:

1) create a solution for each starting position
2) loop through each solution, and find the neighbors of the last element
3) The first solution to reach the end wins.

###### Results

The shortest unique solutions. Works against imperfect mazes.

###### Notes

In CS terms, this is a Breadth-First Search algorithm that is cut short when the first solution is found.

## Shortest Paths Finder

###### The Algorithm

1) create a solution for each starting position
2) loop through each solution, and find the neighbors of the last element
3) a solution reaches the end or a dead end when we mark it by appending a None.
4) clean-up solutions

###### Results

Find all unique solutions. Works against imperfect mazes.

###### Notes

In CS terms, this is a Breadth-First Search algorithm.
It finds all unique, non-looped solutions to the maze.

###### Notes

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

###### Optional Parameters

* *Turn*: String ['left', 'right']
 * Do you want to follow the right wall or the left wall? (default 'right')

###### Results

1 solution only, not the shortest solution

This algorithm does not solve mazes that are not perfect.

###### Notes

To the human brain, this is the easiest possible way to solve a maze. Drunk college kids use this algorithm to solve corn mazes every year. But if we go purely by the number of lines of code, this is one of the hardest maze-solving algorithms to implement on a computer. Neat.


## Vocabulary

1. __biased__ - a maze is biased if there are long runs and corridors more in the North/South or East/West directions.
2. __cell__ - an open passage in the maze
3. __grid__ - the grid is the combination of all passages and barriers in the maze
4. __perfect__ - a maze is perfect if it has one and only one solution
5. __sparse__ - a sparse maze has walls or passages thicker than the usual single unit width
6. __wall__ - an impassable barrier in the maze


#####Go back to the main [README](../README.md)
