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

class LanguageFile(SyntaxTree, paths.ExtendedFilePath):
    """File (leaf of a disk tree, root of contents)"""
    def __init__(self, s, exts=None):
        super.__init__(paths.FilePath, s, exts)
        self._exts = exts if exts else []

    def extended(self, test):
        for ext in self._exts:
            if self._extended(ext):
                return True
            return False
        raise NotMyType(ext)

    def _extended(self, test):
        return self.ext() == test

    def _known_ext(self, ext):
        """Files without extensions can be scripts"""
        if not ext:
            return self.lines()[0][:2] == '#!'
        return ext in self._exts



class ScriptFile(LanguageFile):
    """Script files have text in a known language

    We expect them to have an extension showing their language
    Or be a shebang file
    """
    def __init__(self, s):
        super(ScriptFile, self).__init__(self, s)
        self._shebanged = False

    def _known_ext(self, ext):
        return super(ScriptFile, self)._known_ext(ext) if ext else self._shebang()

    def _shebang(self):
        if not self._shebang:
            self._shebang = self.shebang()
        self._shebanged = bool(self._shebang)
        return self._shebanged


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


class BashScript(ScriptFile, BashNormalSyntaxTree):
    """Syntax tree in a Bash File"""
    def __init__(self):
        super(ScriptFile, self).__init__(self, exts=['.sh', '.bash'])
        super(BashNormalSyntaxTree, self).__init__(self.text())

    def _shebang(self):
        result = super._shebang(self)
        return self._shebang.endswith('bash') if result else False

class JavascriptScript(ScriptFile, JavascriptNormalSyntaxTree):
    """Syntax tree in a Javascript File"""
    def __init__(self):
        super(ScriptFile, self).__init__(self, exts=['.js'])
        super(JavascriptNormalSyntaxTree, self).__init__(self.text())

    def _shebang(self):
        return False


class PythonScript(ScriptFile, PythonNormalSyntaxTree):
    """Syntax tree in a Python File"""
    def __init__(self):
        super(ScriptFile, self).__init__(self, exts=['.py'])
        super(PythonNormalSyntaxTree, self).__init__(self.text())

    def _shebang(self):
        result = super._shebang(self)
        return self._shebang.endswith('python') if result else False

