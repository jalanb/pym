""" "Normal" syntax trees"""


from parse import parse


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


class PythonSyntaxTree():
    """A Python syntax tree"""
    def __init__(self):
        self.tree = parse(self)


class PythonNormalSyntaxTree(NormalSyntaxTree, PythonSyntaxTree):
    """A Normalised Python syntax tree"""
    pass


class PythonFileDiskTree(FileDiskTree, PythonNormalSyntaxTree):
    """Syntax tree in a Python File"""
    def __init__(self):
        super(FileDiskTree, self).__init__(self)
        super(PythonNormalSyntaxTree, self).__init__(self.text())
