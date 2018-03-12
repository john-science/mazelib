# Maze-Solving Algorithms

##### Go back to the main [README](../README.md)


## Blind Alley

###### The Algorithm
1. Scan the maze, identify all fully-connected wall systems.
2. Any wall system that touches the border is not a cul-de-sac, remove it.
3. Determine if remaining wall systems are cul-de-sacs.
4. If so, add a wall segment to turn the cul-de-sac into a dead end.
5. Solve remaining maze using Shortest Paths.

###### Results

* maze-reduction algorithm only, will not solve maze alone

###### Notes

This algorithm is a more flexible version of Cul-de-Sac Filler and Dead End Filler. It can fill or seal the offending portions of the maze, and finds all solutions to even imperfect mazes.


## Chain Algorithm

###### The Algorithm

1. draw a straight-ish line from start to end, ignore the walls.
2. Follow the line from start to end.
    1. If you bump into a wall, you have to go around.
    2. Send out wall-following robots in the 1 or 2 open directions.
    3. If the robot can find your new point, continue on.
    4 .If the robot intersects your line at a point that is further down stream, pick up the path there.
3. repeat step 2 until you are at the end.
    1. If both robots return to their original location and direction, the maze is unsolvable.

###### Optional Parameters

* *Turn*: String ['left', 'right']
 * Do you want to follow the right wall or the left wall? (default 'right')

###### Results

* 1 solution
* not the shortest solution
* works against imperfect mazes

###### Notes

The idea here is that you break the maze up into a sequence of smaller mazes. There are undoubtedly cases where this helps and cases where this is a terrible idea. Caveat emptor.

This algorithm uses the Wall Follower algorithm to solve the sub-mazes. As such, it is significantly more complicated and memory-intensive than your standard Wall Follower.


## Collision Solver

###### The Algorithm

1. step through the maze, flooding all directions equally
2. if two flood paths meet, create a wall where they meet
3. fill in all dead ends
4. repeat until there are no more collisions

###### Results

* finds shortests solutions
* works against imperfect mazes

###### Notes

On a perfect maze, this is little different than the Dead End Filler algorithm. But in heavily braided and imperfect mazes, this algorithm simply iterates over the whole maze a few more times and finds the optimal solutions. It is quite elegant.


## Cul-de-sac Filler

###### The Algorithm

1. Scan the maze, identify all fully-connected wall systems.
2. Any wall system that touches the border is not a cul-de-sac, remove it.
3. Determine if remaining wall systems are cul-de-sacs.
4. If so, add a wall segment to turn the cul-de-sac into a dead end.
5. Solve the remaining maze using Dead End Filler.

###### Results

* maze-reduction algorithm only, will not solve maze alone

###### Notes

This is a classic maze-solving algorithm.  However, it seems to add a lot of complexity to solving a maze. But perhaps if your maze has many cul-de-sacs it would be very helpful.


## Dead End Filler

###### The Algorithm

1. Scan the maze in any order, looking for dead ends.
2. Fill in each dead end, and the dead-end passages attached to them.
3. Use a different solver to build a solution path.

###### Results

* maze-reduction algorithm only, will not solve maze alone

###### Notes

This is a simple Maze solving algorithm.
It focuses on the Maze, is always very fast, and uses no extra memory.

This will always find the one unique solution for perfect Mazes, but won't do much in heavily braid Mazes, and in fact won't do anything useful at all for those Mazes without dead ends.


## Random Mouse

###### The Algorithm:

A mouse just wanders randomly around the maze until it finds the cheese.

###### Results

* 1 solution
* not the shortest solution
* works against imperfect mazes

###### Notes

Random mouse may never finish. Technically. It is certainly inefficient in time, but very efficient in memory.

I added a pruner to the end of this algorithm, to get rid of all unnecessary branches, and backtracks, in the solution.


## Recursive Backtracker

###### The Algorithm:

1) Pick a random direction and follow it
2) Backtrack if and only if you hit a dead end.

###### Results

* 1 solution
* not the shortest solution
* works against imperfect mazes

###### Notes

Mathematically, there is very little difference between this algorithm and Random Mouse. The only difference is that at each point, Random Mouse might go right back where it came from. But Backtracker will only do that if it reaches a dead end.


## Shortest Path Finder

###### The Algorithm:

1) create a possible solution for each neighbor of the starting position
2) find the neighbors of the last element in each solution, branches create new solutions
3) repeat step 2 until you reach the end
4) The first solution to reach the end wins.

###### Results

* finds all solutions
* finds shortest solution(s)
* works against imperfect mazes

###### Notes

In CS terms, this is a Breadth-First Search algorithm that is cut short when the first solution is found.


## Shortest Paths Finder

###### The Algorithm

1) create a possible solution for each neighbor of the starting position
2) find the neighbors of the last element in each solution, branches create new solutions
3) repeat step 2 until you al solutions hit dead ends or reach the end
4) remove all dead end solutions

###### Results

* finds all solutions
* works against imperfect mazes

###### Notes

In CS terms, this is a Breadth-First Search algorithm. It finds all unique, non-looped solutions to the maze.

Though this version is optimized to improve speed, nothing could be done about the fact that this algorithm uses substantially more memory than just the maze grid itself.

## Trémaux's Algorithm

WORK IN PROGRESS


## Wall Follower

###### The Algorithm

Follow the right wall and you will eventually end up at the end.

The details:

1. Choose a random starting direction.
2. At each intersection, take the rightmost turn. At dead-ends, turn around.
3. If you have gone more than (H * W) + 2 cells, stop; the maze will not be solved.
4. Prune the extraneous branches from the solution before returning it.

###### Optional Parameters

* *Turn*: String ['left', 'right']
 * Do you want to follow the right wall or the left wall? (default 'right')

###### Results

* 1 solution
* not the shortest solution
* does not solve imperfect mazes

###### Notes

To the human brain, this is the easiest way to solve a maze. Drunk college kids use this algorithm every year to solve corn mazes. But if we go by the number of lines of code, this is one of the hardest maze-solving algorithms to implement on a computer. Which is really interesting.


## Vocabulary

1. __cell__ - an open passage in the maze
2. __grid__ - the grid is the combination of all passages and barriers in the maze
3. __perfect__ - a maze is perfect if it has one and only one solution
4. __wall__ - an impassable barrier in the maze


##### Go back to the main [README](../README.md)
