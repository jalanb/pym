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


class DocStringer(ast.NodeTransformer):
    def __init__(self):
        ast.NodeTransformer.__init__(self)

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


class Commenter(ast.NodeTransformer):
    """Add comments into an AST"""
    def __init__(self, comments):
        ast.NodeTransformer.__init__(self)
        self.comment = NoComment((-1, -1, ''))
        self.comments = comments
        self.next_comment()

    def next_comment(self):
        try:
            self.comment = Comment(self.comments.pop(0))
        except IndexError:
            self.comment = NoComment((-1, -1, ''))

    def use_comment(self, new_values):
        new_values.append(self.comment)
        self.next_comment()

    def generic_visit(self, node):
        """Visit a node and add any needed comments

        Based on the equivalent method in ast.NodeTransformer which states:
            :copyright: Copyright 2008 by Armin Ronacher
            :license: Python License.
        That license file is in this directory as "PYTHONLICENSE.txt"
        """
        for field, old_value in ast.iter_fields(node):
            old_value = getattr(node, field, None)
            if isinstance(old_value, list):
                new_values = []
                for value in old_value:
                    if isinstance(value, ast.AST):
                        while self.comment.is_line_before(value):
                            self.use_comment(new_values)
                        value = self.visit(value)
                        if value is None:
                            continue
                        if not isinstance(value, ast.AST):
                            new_values.extend(value)
                            continue
                    if statement_precedes_comment(value, self.comment):
                        self.comment.prefix = value
                        self.use_comment(new_values)
                    else:
                        new_values.append(value)
                old_value[:] = new_values
            elif isinstance(old_value, ast.AST):
                new_node = self.visit(old_value)
                if new_node is None:
                    delattr(node, field)
                else:
                    setattr(node, field, new_node)
        return node


def recast_docstrings(tree):
    doc_stringer = DocStringer()
    doc_stringer.visit(tree)


def add_comments(tree, string):
    """Add comments into the tree"""
    comments = get_comments(string)
    commenter = Commenter(comments)
    commenter.visit(tree)
