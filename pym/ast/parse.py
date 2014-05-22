"""Parse source text to an AST"""


import ast


def parse(source, path=None):
    path = path if path else '<unknown>'
    return ast.parse(source, path)
