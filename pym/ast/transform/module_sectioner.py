"""Add comments back in to ASTs"""


import ast


from .transformers import PymTransformer


class Sectioner(PymTransformer):
    """Add sections into a module AST"""
    def __init__(self):
        PymTransformer.__init__(self)

    def handle_old_values(self, old_value):
        if not isinstance(self.node, ast.Module):
            return None
        new_values = []
        for old_value in old_value:
            self.handle_old_value(new_values, old_value)
        return new_values


def add_sections(tree):
    """Add sections into the module tree"""
    sectioner = Sectioner()
    sectioner.visit(tree)
