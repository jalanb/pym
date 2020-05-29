"""Parse source text to an AST"""

import os
import ast
from functools import singledispatch

from pysyte.types.paths import FilePath
from pysyte.types.paths import makepath


def parse_path(source, path):
    return ast.parse(
        source if source else '',
        path if path else '<None>'
    )


@singledispatch
def parse(arg):
    return parse_path(arg, None)


@parse.register(type(None))
def _(arg):
    return parse_path(None, None)


@parse.register(str)
def _(arg):
    try:
        return parse(FilePath(arg))
    except (FileNotFoundError, IOError):
        return parse_path(arg, None)


@parse.register(type(parse_path))
def _(arg):
    line_number = arg.__code__.co_firstlineno
    p = makepath(arg)
    assert p
    astree = parse(p)


@parse.register(type(os))
def _(arg):
    return parse(makepath(arg))


@parse.register(FilePath)
def _(arg):
    return parse_path(arg.text(), arg)
