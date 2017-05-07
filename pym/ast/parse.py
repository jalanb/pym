"""Parse source text to an AST"""


import ast


def parse(source, path=None):
    return ast.parse(source, path or '<None>')


def parse_path(path):
    with open(path) as stream:
        return parse(stream.read(), path)
