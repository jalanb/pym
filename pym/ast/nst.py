""" "Normal" syntax trees"""




import dotsite as site


class SyntaxTree(object):
    """Some kind of Syntax Tree"""
    pass


class DirectoryDiskTree(SyntaxTree, site.paths.DirectoryPath):
    """Directory tree"""
    pass


class LanguageFile(SyntaxTree, site.paths.FilePath):
    """File (leaf of a disk tree, root of contents)"""
    def __init__(self, path, exts=None):
        super(LanguageFile, self).__init__(path, exts)
        self.choose_language(exts)


#  pylint: disable=too-many-ancestors
class ScriptFile(LanguageFile):
    """Script files have text in a known language

    So far we know Python, Bash, JavaScript, English
    """
    def _parse(self):
        self.TODO = True  # raise NotImplementedError

    def __init__(self, path, exts=None):
        super(ScriptFile, self).__init__(self, path, exts=['.py', '.sh', '.js', '.txt'])


class LanguageSyntaxTree(object):
    pass


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
            return self._syntax_tree = self._parse(self)
        except AttributeError:
            self._syntax_tree = self._parse(self)
            return self._syntax_tree

    def tree(self):
        self._n_tree = self._normalise(self.syntax_tree)
        return self._n_tree

    def _normalise(self, node):
        """Convert the syntax tree into a (whatever counts as) Normal (round here) ST"""
        tree = LazyDefaultDict
        tree[node]
        for node in syntax_tree:
            key = node
        self.TODO = True  # raise NotImplementedError


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


class EnglishScript(ScriptFile, EnglishNormalSyntaxTree):
    """Syntax tree in a English File"""
    def __init__(self):
        super(EnglishScript, self).__init__(self, exts=['.txt'])



class BashScript(ScriptFile, BashNormalSyntaxTree):
    """Syntax tree in a Bash File"""
    def __init__(self):
        super(BashScript, self).__init__(self, exts=['.sh', '.bash'])


class JavaScriptScript(ScriptFile, JavaScriptNormalSyntaxTree):
    """Syntax tree in a JavaScript File"""
    def __init__(self):
        super(JavaScriptScript, self).__init__(self, exts=['.js'])


class PythonScript(ScriptFile, PythonNormalSyntaxTree):
    """Syntax tree in a Python File"""
    def __init__(self):
        super(PythonScript, self).__init__(self, exts=['.py'])
