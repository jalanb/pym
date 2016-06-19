"""Script to render a python file

To itself
"""

import os
import sys
import argparse


import render


def parse_args(args=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', help='path to a python file')
    return parser.parse_args(args)


def absolute_python_path(path):
    if not os.path.isfile(path):
        raise ValueError('No such path %r' % path)
    _, ext = os.path.splitext(path)
    if ext != '.py':
        raise ValueError('Extension is not ".py" for %r' % path)
    return os.path.realpath(
        os.path.abspath(os.path.expanduser(os.path.expandvars(path))))


def read_source(path):
    with open(path) as stream:
        return stream.read()


def re_render(path):
    path = absolute_python_path(path)
    string = read_source(path)
    return render.re_render(string)


def main():
    """Render a python file"""
    args = parse_args()
    try:
        print re_render(args.path)
    except ValueError as e:
        print >> sys.stderr, e
        return os.EX_USAGE
    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main())
