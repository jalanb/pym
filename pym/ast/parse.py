"""Parse source text to an AST"""

import os
import ast


def parse(source, path=None):
    if not source and os.path.isfile(path):
        return parse_path(path)
    return ast.parse(source, path or '<None>')


def parse_path(path):
    with open(path) as stream:
        return parse(stream.read(), path)
