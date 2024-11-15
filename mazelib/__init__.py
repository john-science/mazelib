"""Mazelib: a Python tool for creating and solving mazes."""

import importlib.metadata

__version__ = importlib.metadata.version("mazelib")

# ruff: noqa: F401
from mazelib.mazelib import Maze
