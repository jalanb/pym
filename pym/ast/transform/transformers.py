"""Classes which transform ASTs

Provides a class hierarchy of increasing change:
    PymTransformerBase makes no changes
    TreeDecorator adds nodes
    TreeChanger adds or changes nodes, or changes fields
    TreeTransformer adds, changes or deletes nodes or fields
"""

import ast


class PymTransformerBase(ast.NodeVisitor):
    """Base Class for all Pym Transformers

    This class provide generic methods only
        real work is done in inheritors
    """
    def handle_old_values(self, node, values):
        return None

    def handle_value(self, node, field, value):
        pass

    def handle_values(self, node, values):
        new_value = self.handle_old_values(node, values)
        if new_value is not None:
            values[:] = new_value

    def generic_visit(self, node):
        if not isinstance(node, ast.AST):
            return node
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                self.handle_values(node, value)
            elif isinstance(value, ast.AST):
                self.handle_value(node, field, value)
        return node


class TreeDecorator(PymTransformerBase):
    """A decorator is a transformer which only adds

    Nodes or attributes may be added
    This class provide generic methods only
        real work is done in inheritors
    """
    pass


class TreeChanger(TreeDecorator):
    """Transform an AST Node

    Based on ast.NodeTransformer which states:
        :copyright: Copyright 2008 by Armin Ronacher
        :license: Python License.
    That license file is in this directory as "PYTHONLICENSE.txt"
    """

    def before_old_ast_value(self, new_values, value):
        pass

    def add_new_value(self, new_values, value):
        # pylint: disable-msg=no-self-use
        new_values.append(value)

    def handle_new_value(self, new_values, new_value):
        # pylint: disable-msg=no-self-use
        if new_value is None:
            return True
        if not isinstance(new_value, ast.AST):
            new_values.extend(new_value)
            return True
        return False

    def handle_old_non_ast_value(self, new_values, old_value):
        self.add_new_value(new_values, old_value)

    def handle_old_ast_value(self, new_values, old_value):
        self.before_old_ast_value(new_values, old_value)
        new_value = self.visit(old_value)
        if self.handle_new_value(new_values, new_value):
            return
        self.add_new_value(new_values, new_value)

    def handle_old_value(self, new_values, old_value):
        if not isinstance(old_value, ast.AST):
            self.handle_old_non_ast_value(new_values, old_value)
        else:
            self.handle_old_ast_value(new_values, old_value)

    def handle_old_values(self, node, values):
        new_values = []
        for old_value in values:
            self.handle_old_value(new_values, old_value)
        return new_values

    def handle_value(self, node, field, value):
        new_value = self.visit(value)
        if new_value is None:
            delattr(node, field)
        else:
            setattr(node, field, new_value)
