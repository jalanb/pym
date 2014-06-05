"""module to render python asts to text"""

from .renderer import Renderer
from ..ast.parse import parse
from ..ast.transform.commenter import add_comments
from ..ast.transform.reliner import adjust_lines
from ..ast.transform.docstringer import recast_docstrings


def remove_empty_tail(items):
    if not items or items[-1]:
        return items
    for i, item in enumerate(items[::-1]):
        if item:
            return items[:-i]
    return items


def render(node):
    if not node:
        return None
    renderer = Renderer()
    renderer.visit(node)
    return '\n'.join(remove_empty_tail(renderer.lines))


def re_render(string, path=None):
    tree = parse(string, path)
    recast_docstrings(tree)
    add_comments(tree, string)
    adjust_lines(tree)
    text = render(tree)
    if string and text and string[-1] == '\n' and text[-1] != '\n':
        return '%s\n' % text
    return text
