"""Test parsing of code"""


import os
import ast
from unittest import TestCase


from pym.ast import parse


class TestParse(TestCase):
    def test_parse_file(self):
        path = parse.__file__
        stem, _ = os.path.splitext(path)
        path = "%s.py" % stem
        with open(path) as stream:
            source = stream.read()
            parsed = parse.parse_path(source, path)
            self.assertTrue(isinstance(parsed, ast.AST))

    def test_parse_string(self):
        source = "i = 0\ni += 1"
        parsed = parse.parse(source)
        self.assertTrue(isinstance(parsed, ast.AST))

    def test_syntax_error(self):
        source = "i = 0\n    i += 1"
        self.assertRaises(SyntaxError, parse.parse, source)
