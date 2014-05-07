"""module to render python asts to text"""

import ast
import tokenize
from cStringIO import StringIO

from visitors import Renderer
from transformers import DocStringer, Commenter


def get_comments(string):
    """Hold equivalent tokens for a tree being rendered"""
    stream = StringIO(string)
    tokens = list(tokenize.generate_tokens(stream.readline))
    comments = [
        (start_line, start_column, string)
        for type_, string, (start_line, start_column), _, _,
        in tokens
        if type_ == tokenize.COMMENT
    ]
    return sorted(comments)


def parse(source, path=None):
    path = path if path else '<unknown>'
    return ast.parse(source, path)


def find_docstrings(tree):
    doc_stringer = DocStringer()
    doc_stringer.visit(tree)


def add_comments(tree, string):
    """Add comments into the tree"""
    comments = get_comments(string)
    commenter = Commenter(comments)
    commenter.visit(tree)


def render(node):
    renderer = Renderer()
    renderer.visit(node)
    return '\n'.join(renderer.lines)


def re_render(string, path=None):
    tree = parse(string, path)
    find_docstrings(tree)
    add_comments(tree, string)
    return render(tree)
