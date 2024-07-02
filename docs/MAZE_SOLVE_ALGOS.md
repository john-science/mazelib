# Maze-Solving Algorithms

##### Go back to the main [README](../README.md)

Because users are allowed to create and modify mazes in such a great variety of way, the `mazelib` library will only support universal maze-solving algorithms. That is, `mazelib` will not implement any maze-solving algorithm that can't, for instance, solve imperfect mazes (those with loops or more than one solution). Otherwise, the user will have to know internal details about the maze generating / soliving algorithms they use, and if they are compatible.


## Chain Algorithm

###### The Algorithm

1. draw a straight-ish line from start to end, ignore the walls.
2. Follow the line from start to end.
    1. If you bump into a wall, you have to go around.
    2. Send out backtracking robots in the 1 or 2 open directions.
        1. If the robot can find your new point, continue on.
        2. If the robot intersects your line at a point that is further down stream, pick up the path there.
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
* doesn't always work against imperfect mazes

###### Notes

On a perfect maze, this is little different than the Dead End Filler algorithm. But in heavily braided and imperfect mazes, this algorithm simply iterates over the whole maze a few more times and finds the optimal solutions. It is quite elegant.



## Random Mouse

###### The Algorithm:

A mouse just wanders randomly around the maze until it finds the cheese.

###### Results

* 1 solution
* not the shortest solution
* works against imperfect mazes

###### Notes

Random mouse may never finish. Technically. It is certainly inefficient in time, but very efficient in memory.

I highly recommend that this solver run in the default pruning mode, to get rid of all unnecessary branches, and backtracks, in the solution.


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

###### The Algorithm

1) Every time you visit a cell, mark it once.
2) When you hit a dead end, turn around and go back.
3) When you hit a junction you haven't visited, pick a new passage at random.
4) If you're walking down a new passage and hit a junction you have visited, treat it like a dead end and go back.
5) If walking down a passage you have visited before (i.e. marked once) and you hit a junction, take any new passage available, otherwise take an old passage (i.e. marked once).
6) When you finally reach the end, follow cells marked exactly once back to the start.
7) If the Maze has no solution, you'll find yourself at the start with all cells marked twice.

###### Results

* Finds one non-optimal solution.
* Works against imperfect mazes.

###### Notes

This Maze-solving method is designed to be used by a human inside the Maze.


## Vocabulary

1. __cell__ - an open passage in the maze
2. __grid__ - the grid is the combination of all passages and barriers in the maze
3. __perfect__ - a maze is perfect if it has one and only one solution
4. __wall__ - an impassable barrier in the maze


##### Go back to the main [README](../README.md)
