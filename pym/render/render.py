"""module to render python asts to text"""

import ast

from .visitors import Renderer
from ..transform.commenter import add_comments
from ..transform.docstringer import recast_docstrings


def parse(source, path=None):
    path = path if path else '<unknown>'
    return ast.parse(source, path)


def render(node):
    if not node:
        return None
    renderer = Renderer()
    renderer.visit(node)
    return '\n'.join(renderer.lines)


def re_render(string, path=None):
    tree = parse(string, path)
    recast_docstrings(tree)
    add_comments(tree, string)
    text = render(tree)
    if string and text and string[-1] == '\n' and text[-1] != '\n':
        return '%s\n' % text
    return text
