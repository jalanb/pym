""" "Normal" syntax trees"""

import ast

from dotsite import paths

class NST(ast.AST):
    """A normal syntax tree"""
    pass

class DST(NST, paths.DirectoryPath):
    """Directory tree"""
    pass

class FST(NST, paths.FilePath):
    """File tree"""
    pass
