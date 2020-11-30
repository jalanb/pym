"""module to render python asts to text"""

from ast import AST
from pathlib import Path
from functools import singledispatch

from .lines import remove_empty_tail
from .renderer import Renderer
from ..ast.parse import parse
from ..ast.transform.commenter import add_comments
from ..ast.transform.reliner import adjust_lines
from ..ast.transform.docstringer import recast_docstrings


class UnParsable(ValueError):
    pass


def re_render(source, path=None):
    if not source:
        return ""
    tree = parse(source, path)
    if not tree:
        return ""
    recast_docstrings(tree)
    add_comments(tree, source)
    adjust_lines(tree)
    text = render(tree)
    if not text:
        return ""
    return f"{text.rstrip()}\n"


@singledispatch
def render(none: type(None)):
    return None


@render.register
def _(string: str):
    node = parse(string)
    if not node:
        raise UnParsable(string)
    return render(node)


@render.register
def _(node: AST):
    if not node:
        return ""
    renderer = Renderer()
    renderer.visit(node)
    return "\n".join(remove_empty_tail(renderer.lines))


@render.register
def _(path: Path):
    if not path.exists():
        raise UnParsable(str(path))
    node = parse("", path)
    return render(node)


@render.register
def _(method: type(re_render)):
    node = parse(method)
    return render(node)
