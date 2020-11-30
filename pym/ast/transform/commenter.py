"""Add comments back in to ASTs"""

import ast


from .transformers import PymTransformer
from pym.ast.tokens import get_comments
from pym.ast.nodes import Comment, NoComment


def statement_precedes_comment(value, comment):
    return isinstance(value, ast.stmt) and comment.same_line(value)


class Commenter(PymTransformer):
    """Add comments into an AST"""

    def __init__(self, comments):
        PymTransformer.__init__(self)
        self.comment = NoComment((-1, -1, ""))
        self.comments = comments
        self.next_comment()

    def next_comment(self):
        try:
            self.comment = Comment(self.comments.pop(0))
        except IndexError:
            self.comment = NoComment((-1, -1, ""))

    def before_old_ast_value(self, new_values, value):
        while self.comment.is_line_before(value):
            new_values.append(self.comment)
            self.next_comment()

    def add_new_value(self, new_values, value):
        if statement_precedes_comment(value, self.comment):
            self.comment.prefix = value
            new_values.append(self.comment)
            self.next_comment()
        else:
            new_values.append(value)


def add_comments(tree, string):
    """Add comments into the tree"""
    comments = get_comments(string)
    commenter = Commenter(comments)
    commenter.visit(tree)
