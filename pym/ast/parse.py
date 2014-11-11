"""Parse source text to an AST"""


import ast


def parse(source, path=None):
    path = path if path else '<unknown>'
    return ast.parse(source, path)


def parse_path(path):
    with open(path) as stream:
        return parse(stream.read(), path)
