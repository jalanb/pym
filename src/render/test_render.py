"""Test rendering of code"""


import os
import ast
from unittest import TestCase


import render


class TestRender(TestCase):

    def test_parse_file(self):
        path = render.__file__
        stem, _ = os.path.splitext(path)
        path = '%s.py' % stem
        with open(path) as stream:
            source = stream.read()
            parsed = render.parse(source, path)
            self.assertTrue(isinstance(parsed, ast.AST))

    def test_parse_string(self):
        source = 'i = 0\ni += 1'
        parsed = render.parse(source)
        self.assertTrue(isinstance(parsed, ast.AST))

    def test_syntax_error(self):
        source = 'i = 0\n    i += 1'
        self.assertRaises(SyntaxError, render.parse, source)

    def test_render(self):
        expected = 'i = 0\ni += 1'
        node = render.parse(expected)
        actual = render.render(node)
        self.assertEqual(actual, expected)

    def test_render_nothing(self):
        self.assertIsNone(render.render(None))
        self.assertIsNone(render.render(''))

    def test_render_empty(self):
        self.assertFalse(render.render(' '))

    def test_re_render(self):
        path = os.path.dirname(__file__)
        path = os.path.join(path, 'example_source.txt')
        with open(path) as stream:
            expected = stream.read()
            actual = render.re_render(expected, path)
            self.assertEqual(actual, expected)
            expected_lines = expected.splitlines()
            actual_lines = actual.splitlines()
            for expected, actual in zip(expected_lines, actual_lines):
                self.assertEqual(actual, expected)