
from datetime import datetime
from sysconfig import get_python_version
from timeit import Timer

''' The reason that this particular combination of runs was chosen is
    not meant to be obvious.
    A standard set of runs were designed to test the mazelib library
    in the most typical use-case of the target audience.
    The only really important part of this benchmark is that there is a
    standard basis for comparison.
'''
SIZES = [5, 10, 25, 50, 100, 200]
ITERATIONS = [100, 100, 100, 50, 1, 1]
GENERATORS = ['AldousBroder', 'AldousBroder',
              'BacktrackingGenerator', 'BacktrackingGenerator',
              'BinaryTree', 'BinaryTree',
              'Division', 'Division',
              'GrowingTree', 'GrowingTree',
              'HuntAndKill', 'HuntAndKill',
              'Prims', 'Prims',
              'Sidewinder', 'Sidewinder',
              'TrivialMaze', 'TrivialMaze',
              'Wilsons', 'Wilsons']
SOLVERS = ['Collision', 'WallFollower'] * int(len(GENERATORS) / 2)


def main():
    times = run_benchmarks()
    print_benchmarks(times)


def run_benchmarks():
    ''' Run the benchmarks.
        An annoying screen-print will occur so that you know your
        progress, as these tests might take a while.
    '''
    times = [[0.0]*len(SIZES) for _ in range(len(GENERATORS))]

    for row,generator in enumerate(GENERATORS):
        solver = SOLVERS[row]
        print('Run #%d: %s & %s' % (row, generator, solver))
        for col,size in enumerate(SIZES):
            print(col)
            setup = """from mazelib import Maze
from mazelib.solve.%(solv)s import %(solv)s
from mazelib.generate.%(gen)s import %(gen)s
""" % {'solv': solver, 'gen': generator}
            logic = """m = Maze()
m.generator = %(gen)s(%(size)d, %(size)d)
m.solver = %(solv)s()
m.generate()
m.generate_entrances()
m.solve()
""" % {'solv': solver, 'gen': generator, 'size': size}
            t = Timer(logic, setup=setup)
            time = t.timeit(ITERATIONS[col])
            times[row][col] = time

    return times


def print_benchmarks(times):
    ''' Pretty print for the benchmark results,
        with a detailed CSV at the end.
    '''
    print('\nmazelib benchmarking')
    print(datetime.now().strftime('%Y-%m-%d %H:%M'))
    print('Python version: ' + get_python_version())
    print('\nTotal Time (seconds): %.5f\n' %
          sum([sum(times_row) for times_row in times]))

    print('\nmaze size,' + ','.join([str(s) for s in SIZES]))
    for row in range(len(times)):
        method = GENERATORS[row] + '-' + SOLVERS[row] + ','
        print(method + ','.join(['%.5f' % time for time in times[row]]))


if __name__ == '__main__':
    main()
