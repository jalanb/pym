"""module to render python asts to text"""

from ast import AST
from pathlib import Path
from functools import singledispatch

from .lines import remove_empty_tail
from .renderer import Renderer
from ..ast.parse import parse
from ..ast.transform.commenter import add_comments
from ..ast.transform.reliner import adjust_lines
from ..ast.transform.docsourceer import recast_docstrings

class UnParsable(ValueError):
    pass


@singledispatch
def render(string: str):
    node = parse(string) or parse('', string)
    if not node:
        raise UnParsable(string)
    return render(node)


@render.register
def _(node: AST):
    if not node:
        return ''
    renderer = Renderer()
    renderer.visit(node)
    return '\n'.join(remove_empty_tail(renderer.lines))


@render.register
def _(path: Path):
    if not path.exists():
        raise UnParsable(str(path))
    node = parse('', path)
    return render(node)


def re_render(source, path=None):
    tree = parse(source, path)
    recast_docsources(tree)
    add_comments(tree, source)
    adjust_lines(tree)
    text = render(tree)
    if source and text and string[-1] == '\n' and text[-1] != '\n':
        return '%s\n' % text
    return text
