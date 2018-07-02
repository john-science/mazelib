'''
Installing the mazelib package into your system Python is a short process.


To build mazelib and install the package on your computer:
    python setup.py install

To build/install locally, not system-wide:
    python setup.py install --inplace

To force all Cython code to rebuild/reinstall locally:
    python setup.py install --inplace -f

To run the test suit:

    python setup.py test

Though I could not reproduce this, one user reported having to set an environment variable to install:

    export CFLAGS="-I /usr/local/lib/python3.6/site-packages/numpy/core/include"
'''
from setuptools import setup, find_packages
from setuptools.command.install import install
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
from glob import glob
import numpy as np
from os import name as os_name
from sys import argv, platform
from mazelib import __version__

# CONSTANTS
FORCE_FLAGS = ['-f', '--f', '--force']
FORCE_REBUILD = True if any([f in argv for f in FORCE_FLAGS]) else False
IS_WINDOWS = True if (os_name.lower() == 'nt' or 'win' in platform.lower()) else False
COMP_DIRS = {'language_level': 3, 'boundscheck': False, 'initializedcheck': False, 'cdivision': True}

# find all the extension modules in the project
sep = '\\' if IS_WINDOWS else '/'
ext_modules = [Extension(p[:-4].replace(sep, '.'), [p, p[:-2] + 'y'], include_dirs=[np.get_include(), '.'])
               for p in glob(sep.join(['mazelib', '*', '*.pxd']))]


# perform the actual build/install
setup(
    cmdclass={
        'install': install,
        'build_ext': build_ext,
    },
    name='mazelib',
    version=__version__,
    description='A Python API for creating and solving mazes.',
    url='https://github.com/theJollySin/mazelib',
    author='John Stilley',
    classifiers=['Development Status :: 3 - Alpha',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Natural Language :: English',
                 'Topic :: Software Development :: Libraries :: Python Modules'],
    license='GPLv3',
    long_description=open('README.md').read(),
    packages=find_packages(),
    ext_modules=cythonize(ext_modules, annotate=False, force=FORCE_REBUILD, compiler_directives=COMP_DIRS),
    platforms='any',
    test_suite="test",
    install_requires=[
    	"cython",
        "numpy"
    ],
    zip_safe=False)
