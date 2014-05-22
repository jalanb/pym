"""Classes which transform ASTs"""

import ast


from nodes import Comment, NoComment, DocString
from tokens import get_comments


def convert_docstring(node):
    try:
        string = ast.get_docstring(node, clean=True)
    except TypeError:
        string = None
    if string is None:
        return node
    node.body[0] = DocString(node, string)
    return node


class PymTransformer(ast.NodeTransformer):
    """Transform an AST Node

    Based on ast.NodeTransformer which states:
        :copyright: Copyright 2008 by Armin Ronacher
        :license: Python License.
    That license file is in this directory as "PYTHONLICENSE.txt"
    """

    def before_old_ast_value(self, new_values, value):
        pass

    def add_new_value(self, new_values, value):
        # pylint: disable=no-self-use
        new_values.append(value)

    def handle_new_value(self, new_values, new_value):
        # pylint: disable-msg=no-self-use
        if new_value is None:
            return True
        if not isinstance(new_value, ast.AST):
            new_values.extend(new_value)
            return True
        return False

    def handle_old_value(self, new_values, old_value):
        if not isinstance(old_value, ast.AST):
            self.add_new_value(new_values, old_value)
        else:
            self.before_old_ast_value(new_values, old_value)
            new_value = self.visit(old_value)
            if self.handle_new_value(new_values, new_value):
                return
            self.add_new_value(new_values, new_value)

    def handle_list(self, old_value):
        new_values = []
        for old_value in old_value:
            self.handle_old_value(new_values, old_value)
        return new_values

    def handle_item(self, field, node, old_value):
        new_node = self.visit(old_value)
        if new_node is None:
            delattr(node, field)
        else:
            setattr(node, field, new_node)

    def generic_visit(self, node):
        for field, old_value in ast.iter_fields(node):
            if isinstance(old_value, list):
                old_value[:] = self.handle_list(old_value)
            elif isinstance(old_value, ast.AST):
                self.handle_item(field, node, old_value)
        return node


class DocStringer(PymTransformer):
    def __init__(self):
        PymTransformer.__init__(self)

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


def statement_precedes_comment(value, comment):
    return isinstance(value, ast.stmt) and comment.same_line(value)


class Commenter(PymTransformer):
    """Add comments into an AST"""
    def __init__(self, comments):
        PymTransformer.__init__(self)
        self.comment = NoComment((-1, -1, ''))
        self.comments = comments
        self.next_comment()

    def next_comment(self):
        try:
            self.comment = Comment(self.comments.pop(0))
        except IndexError:
            self.comment = NoComment((-1, -1, ''))

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


def recast_docstrings(tree):
    doc_stringer = DocStringer()
    doc_stringer.visit(tree)


def add_comments(tree, string):
    """Add comments into the tree"""
    comments = get_comments(string)
    commenter = Commenter(comments)
    commenter.visit(tree)
