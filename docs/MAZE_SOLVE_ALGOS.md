# Maze-Solving Algorithms

#####Go back to the main [README](../README.md)

## Blind Alley

###### The Algorithm
1. Scan the maze, identify all fully-connected wall systems.
2. Any wall system that touches the border is not a cul-de-sac, remove it.
3. Determine if remaining wall systems are cul-de-sacs.
4. If so, add a wall segment to turn the cul-de-sac into a dead end.
5. Solve remaining maze using Shortest Paths.

###### Results

Removes all cul-de-sacs and dead ends. Does not solve the maze by itself.

###### Notes

This algorithm is a more flexible version of Cul-de-Sac Filler and Dead End Filler. It can fill or seal the offending portions of the maze, and finds all solutions to even imperfect mazes.

## Chain Algorithm

## Collision Solver

## Cul-de-sac Filler

###### The Algorithm
1. Scan the maze, identify all fully-connected wall systems.
2. Any wall system that touches the border is not a cul-de-sac, remove it.
3. Determine if remaining wall systems are cul-de-sacs.
4. If so, add a wall segment to turn the cul-de-sac into a dead end.
5. Solve the remaining maze using Dead End Filler.

###### Results

Removes all cul-de-sacs from a maze. Does not solve a maze by itself.

###### Notes

This is a classic maze-solving algorithm.  However, it seems to add a lot of complexity to solving a maze. But perhaps if your maze has many cul-de-sacs it would be very helpful.

## Dead End Filler

###### The Algorithm

1. Scan the maze in any order, looking for dead ends.
2. Fill in each dead end, and the dead-end passages attached to them.
3. Use a different solver to build a solution path.

###### Results

Finds ALL unique solutions to imperfect mazes.
This algorithm only removes non-solution tiles, another algorithm is needed to build the solution.

###### Notes

This is a simple Maze solving algorithm.
It focuses on the Maze, is always very fast, and uses no extra memory.

This will always find the one unique solution for perfect Mazes, but won't do much in heavily braid Mazes, and in fact won't do anything useful at all for those Mazes without dead ends.

## Djikstra's
## Pledge Algorithm
## Random Mouse

###### The Algorithm:

A mouse just wanders randomly around the maze until it finds the cheese.

###### Results

Yields one solution. The solution will probably not be the shortest. Works against imperfect mazes.

###### Notes

Random mouse may never finish. Technically. It is certainly inefficient in time, but very efficient in memory.

I added a pruner to the end of this algorithm, to get rid of all unnecessary branches, and backtracks, in the solution.

## Recursive Backtracker

###### The Algorithm:

1) Pick a random direction and follow it
2) Backtrack if and only if you hit a dead end.

###### Results

Yields one solution. No gaurantee it will be the shortest. Works against imperfect mazes.

###### Notes

Mathematically, there is very little difference between this algorithm and Random Mouse. The only difference is that at each point, Random Mouse might go right back where it came from. But Backtracker will only do that if it reaches a dead end.


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

In CS terms, this is a Breadth-First Search algorithm. It finds all unique, non-looped solutions to the maze.

Though this version is optimized to improve speed, nothing could be done about the fact that this algorithm uses substantially more memory than just the maze grid itself.

## Trémaux's Algorithm

## Wall Follower

###### The Algorithm

Follow the right wall and you will eventually end up at the end.

The details:

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
