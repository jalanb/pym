"""module to render python asts to text"""

import ast

from visitors import Renderer
from transformers import add_comments, recast_docstrings


def parse(source, path=None):
    path = path if path else '<unknown>'
    return ast.parse(source, path)


def render(node):
    renderer = Renderer()
    renderer.visit(node)
    return '\n'.join(renderer.lines)


def re_render(string, path=None):
    tree = parse(string, path)
    recast_docstrings(tree)
    add_comments(tree, string)
    return render(tree)
