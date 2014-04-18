"""Indentation for renderers"""


INDENT_SIZE = 4


class Indenter:
    """Maintain an indentation count"""
    def __init__(self, string=None):
        self.indent_string = string if string else ' ' * INDENT_SIZE
        self.indentation = 0

    def indent(self):
        self.indentation += 1

    def dedent(self):
        self.indentation -= 1
        if self.indentation < 0:
            raise ValueError('Cannot dedent')

    def render(self, string):
        return '%s%s' % (self.indent_string * self.indentation, string)
