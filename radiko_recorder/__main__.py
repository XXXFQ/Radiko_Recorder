#!/usr/bin/env python3

# Execute with
# $ python -m radiko_recorder

import sys

if __package__ is None and not getattr(sys, 'frozen', False):
    # direct call of __main__.py
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

import radiko_recorder

if __name__ == '__main__':
    radiko_recorder.main()