'''
Installing the mazelib package into your system Python
is a short process:

Optionally, one developer reported having to set an environment variable to his numpy installation:

    export CFLAGS="-I /usr/local/lib/python2.7/site-packages/numpy/core/include"

To build mazelib and install the package:
    python setup.py install
'''

from setuptools import setup


setup(name='mazelib',
    version='0.7',
    description='A Python API for creating and solving mazes.',
    url='https://github.com/theJollySin/mazelib',
    author='John Stilley',
    classifiers=['Development Status :: 3 - Alpha',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Natural Language :: English',
                 'Topic :: Software Development :: Libraries :: Python Modules'],
    license='GPLv3',
    long_description=open('README.md').read(),
    packages=['mazelib',
              'mazelib.generate',
              'mazelib.solve'],
    platforms='any',
    test_suite="test",
    install_requires=[
        "numpy",
    ],
    zip_safe=False)

