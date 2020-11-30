""""Normal" syntax trees"""


from pysyte.types import dictionaries
from pysyte.types import paths


class SyntaxTree(object):
    """Some kind of Syntax Tree"""

    pass


class LanguageSyntaxTree(SyntaxTree):
    """A syntax tree parsed, via a language, from text"""


class EnglishSyntaxTree(LanguageSyntaxTree):
    """An English syntax tree"""

    pass


class BashSyntaxTree(LanguageSyntaxTree):
    """A BASH syntax tree"""

    pass


class JavaScriptSyntaxTree(LanguageSyntaxTree):
    """A JavaScript syntax tree"""

    pass


class PythonSyntaxTree(LanguageSyntaxTree):
    """A Python syntax tree"""

    def _parse(self):
        from pym.ast.parse import parse

        return parse(self)


class NormalSyntaxTree(LanguageSyntaxTree):
    """A normalised syntax tree"""

    @property
    def syntax_tree(self):
        try:
            return self._syntax_tree
        except AttributeError:
            self._syntax_tree = self._parse(self)
            return self._syntax_tree

    def tree(self):
        self._n_tree = self._normalise(self.syntax_tree)
        return self._n_tree

    def _normalise(self, node):
        """Convert the syntax tree into a (whatever counts as) Normal (round here) ST"""
        tree = dictionaries.LazyDefaultDict()
        tree[node.name] = tuple(self._normalise(_) for _ in node.children)
        return tree


class EnglishNormalSyntaxTree(NormalSyntaxTree, EnglishSyntaxTree):
    """A Normalised English syntax tree"""

    pass


class BashNormalSyntaxTree(NormalSyntaxTree, BashSyntaxTree):
    """A Normalised Bash syntax tree"""

    pass


class JavaScriptNormalSyntaxTree(NormalSyntaxTree, JavaScriptSyntaxTree):
    """A Normalised JavaScript syntax tree"""

    pass


class PythonNormalSyntaxTree(NormalSyntaxTree, PythonSyntaxTree):
    """A Normalised Python syntax tree"""

    pass


#  pylint: disable=too-many-ancestors
class ScriptFile(paths.FilePath):
    """Script files have text in a known language"""

    def __init__(self, path, exts):
        super(ScriptFile, self).__init__(path)
        self.exts = exts

    def nst(self):
        ast = self.parse(self.text)
        return self.normalise(ast)


class EnglishScript(ScriptFile, EnglishNormalSyntaxTree):
    """Syntax tree in a English File"""

    def __init__(self):
        super(EnglishScript, self).__init__(self, exts=[".txt"])


class BashScript(ScriptFile, BashNormalSyntaxTree):
    """Syntax tree in a Bash File"""

    def __init__(self):
        super(BashScript, self).__init__(self, exts=[".sh", ".bash"])


class JavaScriptScript(ScriptFile, JavaScriptNormalSyntaxTree):
    """Syntax tree in a JavaScript File"""

    def __init__(self):
        super(JavaScriptScript, self).__init__(self, exts=[".js"])


class PythonScript(ScriptFile, PythonNormalSyntaxTree):
    """Syntax tree in a Python File"""

    def __init__(self):
        super(PythonScript, self).__init__(self, exts=[".py"])
