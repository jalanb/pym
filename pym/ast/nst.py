""" "Normal" syntax trees"""




from dotsite import paths


class SyntaxTree(object):
    """Some kind of Syntax Tree"""
    pass


class DirectoryDiskTree(SyntaxTree, paths.DirectoryPath):
    """Directory tree"""
    pass


class NotMyType(ValueError):
    pass

class LanguageFile(SyntaxTree, paths.FilePath):
    """File (leaf of a disk tree, root of contents)"""
    def __init__(self, s, exts=None):
        super.__init__(paths.FilePath, s)
        assert self.extend(self.extension)
        self._exts = exts if exts else []

    def self.extend(self, ext):
        if not _known_ext(ext):
            raise NotMyType(ext)

    def _known_ext(self, ext):
        """Files without extensions can be scripts"""
        if not ext:
            return self.lines()[0][:2] == '#!'
        return ext in self._exts


class LanguageSyntaxTree(object):
    def _parse(self, string):
        raise NotImplementedError

class BashSyntaxTree(LanguageSyntaxTree):
    """A BASH syntax tree"""
    pass


class JavascriptSyntaxTree(LanguageSyntaxTree):
    """A JavaScript syntax tree"""
    pass


class PythonSyntaxTree(LanguageSyntaxTree):
    """A Python syntax tree"""
    def _parse(self):
        from parse import parse
        return parse(self))


class NormalSyntaxTree(LanguageSyntaxTree):
    """A normal syntax tree"""
    def normalize(self):
        tree = self._parse(self)
        return self._normal(tree)

    def _normal(self, tree):
        raise NotImplementedError


class BashNormalSyntaxTree(NormalSyntaxTree, BashSyntaxTree):
    """A Normalised Bash syntax tree"""
    def _normal(self, ast):
        """Convert the Bashic AST into a (whatever counts as) Normal (round here) ST"""
        raise NotImplementedError


class JavaScriptNormalSyntaxTree(NormalSyntaxTree, JavaScriptSyntaxTree):
    """A Normalised JavaScript syntax tree"""
    def _normal(self, ast):
        """Convert the JavaScriptic AST to an NST"""
        raise NotImplementedError


class PythonNormalSyntaxTree(NormalSyntaxTree, PythonSyntaxTree):
    """A Normalised Python syntax tree"""
    def _normal(self, ast):
        """Convert the Pythonic AST to an NST"""
        raise NotImplementedError


class BashFileDiskTree(LanguageFile, BashNormalSyntaxTree):
    """Syntax tree in a Bash File"""
    def __init__(self):
        super(LanguageFile, self).__init__(self, exts=['.sh', '.bash'])
        super(BashNormalSyntaxTree, self).__init__(self.text())


class JavascriptFileDiskTree(LanguageFile, JavascriptNormalSyntaxTree):
    """Syntax tree in a Javascript File"""
    def __init__(self):
        super(LanguageFile, self).__init__(self, exts=['.js'])
        super(JavascriptNormalSyntaxTree, self).__init__(self.text())


class PythonFileDiskTree(LanguageFile, PythonNormalSyntaxTree):
    """Syntax tree in a Python File"""
    def __init__(self):
        super(LanguageFile, self).__init__(self, exts=['.py'])
        super(PythonNormalSyntaxTree, self).__init__(self.text())
