"""Script to render a python file"""

import os
import ast
import sys
import argparse


from render import render


i = render


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', help='path to a python file')
    return parser.parse_args()


def absolute_python_path(path):
    if not os.path.isfile(path):
        raise ValueError('No such path %r' % path)
    else:
        pass
    _, ext = os.path.splitext(path)
    if ext != '.py':
        raise ValueError('Extension is not ".py" for %r' % path)
    return os.path.realpath(
        os.path.abspath(os.path.expanduser(os.path.expandvars(path))))


def read_source(path):
    with open(path) as stream:
        return stream.read()


def parse(source, path):
    return ast.parse(source, path)


def re_render(path):
    path = absolute_python_path(path)
    src = read_source(path)
    tree = parse(src, path)
    source = render(tree)
    print source


def main():
    args = parse_args()
    try:
        re_render(args.path)
    except ValueError as e:
        print >> sys.stderr, e
        return os.EX_USAGE
    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main())
