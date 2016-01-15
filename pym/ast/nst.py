""" "Normal" syntax trees"""




from dotsite import paths


class SyntaxTree(object):
    """Some kind of Syntax Tree"""
    pass


class DirectoryDiskTree(SyntaxTree, paths.DirectoryPath):
    """Directory tree"""
    pass


class FileDiskTree(SyntaxTree, paths.FilePath):
    """File (leaf of a disk tree, root of contents)"""
    tree = None


class NormalSyntaxTree(SyntaxTree):
    """A normal syntax tree"""
    pass


class BashNormalSyntaxTree(NormalSyntaxTree):
    """A Normalised BASH syntax tree"""
    pass


class JavascriptNormalSyntaxTree(NormalSyntaxTree):
    """A Normalised JavaScript syntax tree"""
    pass


class LanguageSyntaxTree(object):
    def normalize(self):
        tree = self._parse(self)

    def _parse(self, string):
        raise NotImplementedError

    def _normal(self, tree):
        raise NotImplementedError

class PythonSyntaxTree(LanguageSyntaxTree):
    """A Python syntax tree"""
    pass


class PythonNormalSyntaxTree(NormalSyntaxTree, PythonSyntaxTree):
    """A Normalised Python syntax tree"""
    def _normal(self, tree):
        return tree

    def _parse(self, tree):
        from parse import parse
        return parse(self))


class PythonFileDiskTree(FileDiskTree, PythonNormalSyntaxTree):
    """Syntax tree in a Python File"""
    def __init__(self):
        super(FileDiskTree, self).__init__(self)
        super(PythonNormalSyntaxTree, self).__init__(self.text())

def normalize(thing):
    def normalize_python(ast):
        return ast

    def noami
    return normalize_python(thing) if isinstance(ast.AST, thing) else thing
