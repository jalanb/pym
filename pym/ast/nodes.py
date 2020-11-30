"""Decorative nodes for ASTs"""

import ast


class BlankLine(ast.stmt):
    pass


class DocString(ast.Str):
    def __init__(self, node, string):
        ast.Str.__init__(self)
        self.lineno = getattr(node, "lineno", 0)
        self.col_offset = 0
        self.s = string


class Comment(ast.stmt):
    def __init__(self, comment):
        ast.stmt.__init__(self)
        line, column, string = comment
        self.lineno = line
        self.col_offset = column
        self.s = string
        self.prefix = None

    def is_line_before(self, node):
        if not hasattr(node, "lineno"):
            return False
        if self.lineno < node.lineno:
            return True
        return False

    def same_line(self, node):
        try:
            return self.lineno == node.lineno
        except AttributeError:
            return False

    def is_before(self, node):
        if self.is_line_before(node):
            return True
        if self.same_line(node):
            return self.col_offset < node.col_offset
        return False

    def set_prefix(self, statement):
        self.prefix = statement


class NoComment(Comment):
    def is_line_before(self, _):
        return False
