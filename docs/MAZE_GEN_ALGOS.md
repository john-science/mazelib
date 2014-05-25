# Maze-Generating Algorithms

#####Go back to the main [README](../README.md)


## Aldous-Broder

###### The Algorithm

1. Choose a random cell.
2. Choose a random neighbor of the current cell and visit it. If the neighbor has not yet been visited, add the traveled edge to the spanning tree.
3. Repeat step 2 until all cells have been visited.

###### Notes

Results: perfect, unbiased

This is one of the slowest maze-generating algorithms. But it produces nice mazes.

The Aldous-Broder algorithm treats the cells of a maze as a graph, and solves to find a Uniform Spanning Tree that covers that graph.

## Backtracking

###### The Algorithm

1. Randomly choose a starting cell.
2. Randomly choose a wall at the current cell and open a passage through to any random adjacent cell, that has not been visited yet. This is now the current cell.
3. If all adjacent cells have been visited, back up to the previous and repeat step 2.
4. Stop when the algorithm has backed all the way up to the starting cell.

###### Notes

Results: perfect, unbiased

This is a standard maze-generation algorithm because it is easy to understand and implement. And it produces high-quality mazes.

## Binary Tree

###### The Algorithm

1. For every cell in the grid, knock down a wall either North or West.

It does not matter what order you go through all the cells in the grid. And if you are on the North edge of the grid, you will have to carve West.

###### Notes

Results: perfect, biased, flawed

This algorithm produces mazes with a serious flaw: the North and West borders of the maze are completely open. This makes solving the maze too easy to be fun. That is, unless the person solving the maze can't see the whole thing at one time. In which case, this algorithm is still useful.

On the positive side, this algorithm is extremely fast and very easy to implement.

## Cellular Automaton

###### The Algorithm

Cells survive if they have one to four neighbours. If a cell has exactly three neighbours, it is born. It is similar to Conway's Game of Life in that patterns that do not have a living cell adjacent to 1, 4, or 5 other living cells in any generation will behave identically to it.

###### Notes

Results: perfect, unbiased

Using Cellular Automation to generate a maze is a really fun idea, and it is even reasonably fast. And the result is a "perfect" maze, but not always the hardest maze. Generating a few of these mazes, you begin to see that the results are frequently quick easy to solve.

More research is needed to create a post-processing step to remove the typical Cellular Automaton defects.

## Eller's

###### The Algorithm

1. Put the cells of the first row each in their own set.
2. Join adjacent cells. But not if they are already in the same set.
    Merge the sets of these cells.
3. For each set in the row, create at least one vertical connection down to the next row.
4. Put any unconnected cells in the next row into their own set.
5. Repeast until the last row.
6. In the last row, join all adjacent cells that do not share a set.

###### Notes

Results: perfect, unbiased

This is a classic set-theory algorithm. It is not the fastest algorithm, as it requires relabeling whole sets of cells at every step.

But this algorithm does have the fun advantage of being easy to bias in the X or Y directions with two little numbers: xbias and ybias, each between zero and one (0.5 is unbiased).

## Growing Tree

###### The Algorithm

1. Let C be a list of cells, initially empty. Add one cell to C, at random.
2. Choose a cell from C, and carve a passage to any unvisited neighbor of that cell, adding that neighbor to C as well. If there are no unvisited neighbors, remove the cell from C.
3. Repeat step 2 until C is empty.

###### Notes

Results: perfect, unbiased

This algorithm is very flexible. Instead of defining exactly what must be done, it lays out a general construct. The exact order in which we choose a new cell from set C in step 2 is left undefined. That means we can pick on at random (and mimick the Prim's algorithm), or always pick the most recent one (and mimick the Backtracking algorithm). The implementation here allows the developer to set the percentage of time Backtracking is chosen versus Prim's. This gives a lot of variety to the final complexity and look of the final maze.

## Hunt-and-Kill

###### The Algorithm

1. Randomly choose a starting cell.
2. Perform a random walk from the current cel, carving passages to unvisited neighbors, until the current cell has no unvisited neighbors.
3. Select a new grid cell; if it has been visited, walk from it.
4. Repeat steps 2 and 3 a sufficient number of times that there the probability of a cell not being visited is extremely small.

###### Notes

Results: perfect, unbiased

Generally, you might think random-walk algorithms are very slow. But Hunt-and-Kill is quite efficient. And I really like the end results of this algorithm, the mazes are not easy to solve.
In this implementation of Hunt-and-kill there are two different ways to select a new grid cell in step 2.  The first is serpentine through the grid (the classic solution), the second is to randomly select a new cell enough times that the probability of an unexplored cell is very, very low. The second option includes a small amount of risk, but it creates a more interesting, harder maze. So the second option is default in this implementation.

## Kruskal's

###### The Algorithm

1. Create a set of all walls in the grid.
2. Randomly select a wall from the grid. If that wall connects two disjoint trees, join the trees. Otherwise, throw that wall away.
3. Repeat step 2 until there are no more walls left in the set.

###### Notes

Results: perfect, unbiased

Like Prim's, it is based on a namesake algorithm for finding a Minimal Spanning Tree (MST) over a graph.

## Monte Carlo

###### The Algorithm

TBA

###### Notes

There's an old joke that particle physicists use Monte Carlo modeling to solve all their problems: where to eat lunch, finding love, everything.

Well, I guess I was at Fermliab too long. This is an original algorithm, using the first algorithm I ever learned in software. (I may work on creating a Las Vegas algorithm variation).

## Prim's

###### The Algorithm

1. Choose an arbitrary cell from the grid, and add it to some (initially empty) set visited nodes (V).
2. Randomly select a wall from the grid, that connects a cell in V with another cell not in V.
3. Add that wall to the Minimal Spanning Tree (MST), and the edge’s other cell to V.
4. Repeat steps 2 and 3 until V includes every cell in G.

###### Notes

Results: perfect, unbiased

This is a classic. Like Kruskal's, it is based on the idea of finding a MST in a graph. But Prim's is purely random. In fact, randomized variations on other maze-generating algorithms are frequently called "Prim's variations".

## Recursive Division

###### The Algorithm

1. Start with an empty grid.
2. Bisect the grid with a wall (horizontal or vertical). Add a single passage through the wall.
3. Repeat step 2 with the areas on either side of the wall.
4. Continue, recursively, until the maze passages are the desired resolution.

###### Notes

Results: perfect, biased

The algorithm is very simple to understand, and reasonably simple to implement. But the results will always look skewed. A big line that perfect divides a maze makes it easier for the human eye to solve a maze: we can quickly reduce our search space. This is doubly true for humans that happen to know the maze was created by division.

This implementation tries, as far as is possible, to reduce these biases by alternating the cuts between horizontal and vertical. (Obviously, if you made 7 vertical cuts in a row the maze would be very easy to solve.)


## Sidewinder

###### The Algorithm

1. Work through the grid row-wise, starting with the cell at 0,0.
2. Add the current cell to a “run” set.
3. For the current cell, randomly decide whether to carve East.
4. If a passage East was carved, make the new cell the current cell and repeat steps 2-4.
5. If a passage East was not carved, choose any one of the cells in the run set and carve a passage North. Then empty the run set. Repeat steps 2-5.
6. Continue until all rows have been processed.

This implementation has an optional bias parameter: [0.0, 1.0]. If the bias is set less than 0.5 the maze will be biased East-West, if it set greater than 0.5 it will be biased North-South.

###### Notes

Results: perfect, unbiased, flawed

The algorithm is simple and optimally fast. However, the North side of the maze will always be one, long, open corridor. For my tastes, this makes the maze too easy to solve. There are use-cases where that will not matter though.

Active research is underway to create a post-processing step to fix this issue.


## Wilson's

###### The Algorithm

1. Choose a random cell and add it to the Uniform Spanning Tree (UST).
2. Select any cell that is not in the UST and perform a random walk until you find a cell that is.
3. Add the cells and walls visited in the random walk to the UST.
4. Repeat steps 2 and 3 until all cells have been added to the UST.

###### Notes

Results: perfect, unbiased

Like all random-walk algorithms, Wilson's isn't terribly fast. However, this still converges faster than Aldous-Broder.


#####Go back to the main [README](../README.md)

