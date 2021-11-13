""" The benchmarks below are useful for testing performance when making changes to the maze algorithms. """
from datetime import datetime
from sysconfig import get_python_version
from timeit import Timer
from mazelib import __version__ as version

# CONFIG
SIZES = [5, 10, 25, 50, 100]
ITERATIONS = [100, 50, 20, 5, 1]
GENERATORS = [
    "AldousBroder",
    "BacktrackingGenerator",
    "BinaryTree",
    "HuntAndKill",
    "Prims",
    "Sidewinder",
    "TrivialMaze",
    "Wilsons",
]
SOLVERS = ["Collision", "Tremaux"]


def main():
    times = run_benchmarks()
    print_benchmarks(times)


def run_benchmarks():
    """Run the benchmarks.
    An annoying screen-print will occur so that you know your progress, as these tests might take a while.

    Returns:
        list: 2D list of the team each generator/solver combination took
    """
    times = [[0.0] * len(SIZES) for _ in range(len(GENERATORS) * len(SOLVERS))]

    row = -1
    for generator in GENERATORS:
        for solver in SOLVERS:
            row += 1
            print("Run #%d: %s & %s" % (row, generator, solver))
            for col, size in enumerate(SIZES):
                print(col)
                setup = """from mazelib import Maze
from mazelib.solve.%(solv)s import %(solv)s
from mazelib.generate.%(gen)s import %(gen)s
""" % {
                    "solv": solver,
                    "gen": generator,
                }
                logic = """m = Maze()
m.generator = %(gen)s(%(size)d, %(size)d)
m.solver = %(solv)s()
m.generate()
m.generate_entrances()
m.solve()
""" % {
                    "solv": solver,
                    "gen": generator,
                    "size": size,
                }
                t = Timer(logic, setup=setup)
                time = t.timeit(ITERATIONS[col])
                times[row]
                times[row][col] = time

    return times


def print_benchmarks(times):
    """Pretty print for the benchmark results, with a detailed CSV at the end.

    Args:
        times (list): timing results for the benchmark runs
    Results: None
    """
    print("\nmazelib benchmarking")
    print(datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("Python version: {0}".format(get_python_version()))
    print("mazelib version: {0}".format(version))
    print(
        "\nTotal Time (seconds): %.5f\n" % sum([sum(times_row) for times_row in times])
    )
    print("\nmaze size," + ",".join([str(s) for s in SIZES]))

    row = -1
    for generator in GENERATORS:
        for solver in SOLVERS:
            row += 1
            method = generator + "-" + solver + ","
            print(method + ",".join(["%.5f" % time for time in times[row]]))


if __name__ == "__main__":
    main()
