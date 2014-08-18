"""Add comments back in to ASTs"""


import ast


from .transformers import PymTransformerBase
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
    raise ValueError('Ungroupable')


def _add_blank_lines(nodes):
    previous_id = 0
    result = []
    for node in nodes:
        group_id = module_node_group_id(node)
        if group_id != previous_id and previous_id != None:
            result.append(BlankLine())
            result.append(BlankLine())
            previous_id = group_id
        result.append(node)
    return result


class Liner(PymTransformerBase):
    """Add lines into a module AST"""
    def __init__(self):
        PymTransformerBase.__init__(self)

    def handle_old_values(self, node, values):
        if not isinstance(node, ast.Module):
            return None
        return _add_blank_lines(values)


def adjust_lines(tree):
    """Add lines into the module tree"""
    liner = Liner()
    liner.visit(tree)
