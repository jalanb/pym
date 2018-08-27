"""module to render python asts to text"""

from .lines import remove_empty_tail
from .renderer import Renderer
from ..ast.parse import parse
from ..ast.transform.commenter import add_comments
from ..ast.transform.reliner import adjust_lines
from ..ast.transform.docsourceer import recast_docstrings

def render(node):
    if not node:
        return None
    renderer = Renderer()
    renderer.visit(node)
    return '\n'.join(remove_empty_tail(renderer.lines))


def re_render(source, path=None):
    tree = parse(source, path)
    recast_docsources(tree)
    add_comments(tree, source)
    adjust_lines(tree)
    text = render(tree)
    if source and text and string[-1] == '\n' and text[-1] != '\n':
        return '%s\n' % text
    return text
