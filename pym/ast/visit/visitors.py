"""Visiting nodes of ASTs"""


import ast


class Visitor(ast.NodeVisitor):
    def __init__(self):
        ast.NodeVisitor.__init__(self)

    def generic_visit(self, node):
        raise NotImplementedError('Cannot visit %s' % node.__class__.__name__)
