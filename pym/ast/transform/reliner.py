"""Add comments back in to ASTs"""


import ast


from .transformers import PymTransformer
from ..nodes import DocString, BlankLine


def module_node_group_id(node):
    if isinstance(node, DocString):
        return 0
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        return 1
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        return id(node)
    if isinstance(node, ast.stmt):
        return 2
    raise ValueError("Ungroupable")


def _add_blank_lines(nodes):
    previous_id = 0
    result = []
    for node in nodes:
        group_id = module_node_group_id(node)
        if previous_id and group_id != previous_id:
            result.append(BlankLine())
            result.append(BlankLine())
            previous_id = group_id
        result.append(node)
    return result


class Liner(PymTransformer):
    """Add lines into a module AST"""

    def __init__(self):
        PymTransformer.__init__(self)

    def handle_old_values(self, old_values):
        if not isinstance(self.node, ast.Module):
            return None
        return _add_blank_lines(old_values)


def adjust_lines(tree):
    """Add lines into the module tree"""
    liner = Liner()
    liner.visit(tree)
