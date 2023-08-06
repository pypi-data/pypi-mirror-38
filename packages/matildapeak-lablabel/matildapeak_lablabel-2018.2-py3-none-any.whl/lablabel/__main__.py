#!/usr/bin/env python3

"""An entry-point that allows the module to be executed.
This also simplifies the distribution as this is the
entry-point for the console script (see setup.py).
"""

import sys
from .lablabel import main as lablabel_main


def main():
    """The entry-point of the component."""
    return lablabel_main()


if __name__ == '__main__':
    sys.exit(main())
