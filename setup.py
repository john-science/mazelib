'''
Installing the mazelib package into your system Python
is a short process:

Optionally, one developer reported having to set an environment variable to his numpy installation:

    export CFLAGS="-I /usr/local/lib/python3.6/site-packages/numpy/core/include"

To build mazelib and install the package on your computer:
    python setup.py install

To build/install locally, not system-wide:
    python setup.py install --inplace

To force all Cython code to rebuild/reinstall locally:
    python setup.py install --inplace --f

To run the test suit:

    python setup.py test
'''
from setuptools import setup, find_packages
from setuptools.command.install import install
from distutils.extension import Extension
from Cython.Distutils import build_ext as build_pyx
from Cython.Build import cythonize
from glob import glob
import numpy as np
from os import name as os_name
from sys import argv, platform

# CONSTANTS
FORCE_REBUILD = True if "-f" in argv else False
IS_WINDOWS = True if (os_name.lower() == 'nt' or 'win' in platform.lower()) else False


class InstallCommand(install):
    def run(self):
        add_version()
        try:
            install.run(self)
        except Exception as err:
            print(('Error performing egg install : {0}'.format(err)))
        finally:
            clear_version()
        

# find all the extension modules in the project
sep = '\\' if IS_WINDOWS else '/'
ext_modules = [Extension(p[:-4].replace(sep, '.'), [p, p[:-2] + 'y'], include_dirs=[np.get_include(), '.']) for p in glob('mazelib/*/*.pxd')]


setup(
    cmdclass={
        'install': InstallCommand,
        'build_ext': build_pyx,
    },
    name='mazelib',
    version='0.8',
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
    ext_modules=cythonize(ext_modules, annotate=True, force=FORCE_REBUILD),
    platforms='any',
    test_suite="test",
    install_requires=[
    	"cython"
        "numpy",
    ],
    zip_safe=False)
