"""Test rendering of code"""


import os
import ast
from fnmatch import fnmatch
from unittest import TestCase


from pym.rendering import render
from pym.ast.parse import parse


def path_hence(sub_path):
    path = os.path.dirname(__file__)
    return os.path.join(path, sub_path)


def get_source_here(sub_path):
    with open(sub_path) as stream:
        return path, stream.read()


class TestRender(TestCase):
    def test_parse_file(self):
        path = render.__file__
        stem, _ = os.path.splitext(path)
        path = "%s.py" % stem
        with open(path) as stream:
            source = stream.read()
            parsed = parse(source, path)
            self.assertTrue(isinstance(parsed, ast.AST))

    def test_parse_string(self):
        source = "i = 0\ni += 1"
        parsed = parse(source)
        self.assertTrue(isinstance(parsed, ast.AST))

    def test_syntax_error(self):
        source = "i = 0\n    i += 1"
        self.assertRaises(SyntaxError, parse, source)

    def test_render(self):
        expected = "i = 0\ni += 1"
        node = parse(expected)
        actual = render.render_node(node)
        self.assertEqual(actual, expected)

    def test_render_nothing(self):
        self.assertIsNone(render.render_node(None))

    def test_render_nostrings(self):
        self.assertIsNone(render.render_string(None))
        self.assertIsNone(render.render_string(""))
        self.assertFalse(render.render_string(" "))

    def test_render_string(self):
        path, source = get_source_here("re_render.txt")
        expected = source
        actual = render.render_string(source, path)
        self.assertEqual(expected, actual)

    def test_render_path(self):
        path, source = get_source_here("re_render.txt")
        expected = render.render_string(source, path)
        actual = render.render_path(path)

    def test_examples(self):
        there = os.path.join(os.path.dirname(__file__), "examples")
        examples = [f for f in os.listdir(there) if fnmatch(f, "*.py")]
        for example in examples:
            example, source = get_source_here("examples/%s" % example)
            actual = render.render_string(source, example)
            # Compare results line by line for better error messaging
            source_lines = source.splitlines()
            actual_lines = actual.splitlines()
            lines = zip(source_lines, actual_lines)
            for i, (expected, actual) in enumerate(lines):
                name = os.path.basename(example)
                message = "%s, %s: %r != %r" % (name, i, expected, actual)
                self.assertEqual(expected, actual, message)

    def test_unknown_node(self):
        class JustInventedThisNow(ast.Str):
            pass

        testable = JustInventedThisNow()
        renderer = render.Renderer()
        self.assertRaises(NotImplementedError, renderer.visit, testable)
