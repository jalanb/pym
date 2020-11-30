"""Indentation for renderers"""


INDENT_SIZE = 4


class Indenter(object):
    """Maintain an indentation count"""

    def __init__(self, string=None):
        self.indent_string = string if string else " " * INDENT_SIZE
        self.indentation = 0

    def __str__(self):
        return self.indent_string * self.indentation

    def _check(self):
        if self.indentation >= 0:
            return
        self.indentation = 0
        message = "Negative indentation: %d" % self.indentation
        raise ValueError(message)

    def indent(self):
        self._check()
        self.indentation += 1

    def dedent(self):
        self.indentation -= 1
        self._check()

    def render(self, string):
        return "%s%s" % (self, string)
