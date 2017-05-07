"""Visiting nodes of ASTs"""


import ast
import linecache


class Visitor(ast.NodeVisitor):
    def __init__(self):
        super(Visitor, self).__init__()

    def generic_visit(self, node):
        raise NotImplementedError('Cannot visit %s' % node.__class__.__name__)


class Sourcer(Visitor):
    def __init__(self):
        super(Sourcer, self).__init__()

    def generic_visit(self, node):
        line_number = node.lineno
        line = linecache.getline(filename, line_number).rstrip()
