"""Test rendering of code"""


import os
import ast
from fnmatch import fnmatch
from unittest import TestCase


from pym.render import render


def get_source_here(source):
    path = os.path.dirname(__file__)
    path = os.path.join(path, source)
    with open(path) as stream:
        return path, stream.read()

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
        path, expected = get_source_here('re_render.txt')
        actual = render.re_render(expected, path)
        self.assertEqual(expected, actual)

    def test_examples(self):
        there = os.path.join(os.path.dirname(__file__), 'examples')
        examples = [f for f in os.listdir(there) if fnmatch(f, '*.py')]
        for example in examples:
            example, expected = get_source_here('examples/%s' % example)
            actual = render.re_render(expected, example)
            expected_lines = expected.splitlines()
            actual_lines = actual.splitlines()
            lines = zip(expected_lines, actual_lines)
            for i, (expected, actual) in enumerate(lines):
                name = os.path.basename(example)
                message = '%s, %s: %r != %r' % (name, i, expected, actual)
                self.assertEqual(expected, actual, message)

