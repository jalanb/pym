"""Distinguish docstrings in ASTs"""

import ast


from pym.ast.nodes import DocString
from .transformers import PymTransformerBase


def convert_docstring(node):
    try:
        string = ast.get_docstring(node, clean=True)
    except TypeError:
        string = None
    if string is None:
        return node
    node.body[0] = DocString(node, string)
    return node


def recast_docstrings(tree):
    doc_stringer = DocStringer()
    doc_stringer.visit(tree)


class DocStringer(PymTransformerBase):
    def __init__(self):
        PymTransformerBase.__init__(self)

    def generic_visit(self, node):
        """Visit a node and convert first string to a docstring"""
        node = convert_docstring(node)
        if isinstance(node, ast.AST):
            for _, value in ast.iter_fields(node):
                if isinstance(value, list):
                    for item in value:
                        self.visit(item)
                elif isinstance(value, ast.AST):
                    self.visit(value)
        return node
