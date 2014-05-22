"""Classes which transform ASTs"""

import ast


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
