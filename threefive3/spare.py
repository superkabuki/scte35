"""
stuff.py functions and such common to threefive3.
"""

from sys import stderr


def print2(gonzo=b""):
    """
    print2 prints to 2 aka stderr.
    """
    print(gonzo, file=stderr, flush=True)
