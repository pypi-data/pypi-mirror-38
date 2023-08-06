from __future__ import absolute_import
import os
import sys


if __package__ == '':
    # first dirname call strips of '/__main__.py'
    # Resulting path is the name of the wheel itself
    # Add that to sys.path so we can import our module
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

from make_django.main import main as _main

if __name__ == '__main__':
    sys.exit(_main())