# Maze-Transmuting Algorithms

##### Go back to the main [README](../README.md)


## Cul-de-sac Filler

###### The Algorithm

1. Scan the maze, looking for cells with connecting halls that go in exactly two directions.
2. At each of these places, travel in both directions until you find your first intersection.
3. If the first intersection for both paths is the same, you have a loop.
4. Fill in the cell you started at with a wall, breaking the loop.

###### Results

* This works great for simple loops, and even multi-loops. It would probably fail for big, empty rules.

###### Notes

This is a classic algorithm. However, it seems fairly slow by design. Still, if your maze has many cul-de-sacs / loops it could be very helpful.


## Dead End Filler

###### The Algorithm

1. Scan the maze in any order, looking for dead ends.
2. Fill in each dead end, and the dead-end passages attached to them.

###### Results

* Run this algorithm enough times on a perfect maze and it will leave only the solution cells open!

###### Notes

If you generate a maze which is just *all* loops (called a heavily braided maze), this algorithm won't do much. But it nearly all other scenarios it works like a charm.


## Vocabulary

1. __cell__ - an open passage in the maze
2. __grid__ - the grid is the combination of all passages and barriers in the maze
3. __perfect__ - a maze is perfect if it has one and only one solution
4. __wall__ - an impassable barrier in the maze


##### Go back to the main [README](../README.md)
