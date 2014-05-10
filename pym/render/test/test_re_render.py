"""Test re-rendering"""


import os
from unittest import TestCase


from pym.render import re_render


class ReRenderTest(TestCase):
    def setUp(self):
        pass

    def test_parse_args(self):
        expected = __file__
        args = re_render.parse_args([expected])
        self.assertEqual(args.path, expected)

    def test_no_args(self):
        self.assertRaises(SystemExit, re_render.parse_args)

    def test_absolute_python_path(self):
        stem, _ = os.path.splitext(__file__)
        expected = '%s.py' % stem
        actual = re_render.absolute_python_path(expected)
        self.assertEqual(expected, actual)

    def test_absolute_bad_path(self):
        self.assertRaises(
            ValueError, re_render.absolute_python_path, '/no/such/path')

    def test_absolute_non_python_path(self):
        """Test that a file which is not python source raises ValueError

        We need a file which exists, but is not ...py
            Use the compiled (.pyc) version of this file
        """
        stem, _ = os.path.splitext(__file__)
        compiled_path = '%s.pyc' % stem
        self.assertRaises(
            ValueError, re_render.absolute_python_path, compiled_path)

    def test_read_source(self):
        stem, _ = os.path.splitext(__file__)
        python_path = '%s.py' % stem
        source_text = re_render.read_source(python_path)
        self.assertTrue('test_read_source' in source_text)

    def test_re_render(self):
        stem, _ = os.path.splitext(re_render.__file__)
        python_path = '%s.py' % stem
        expected = re_render.read_source(python_path)
        actual = re_render.re_render(python_path)
        self.assertEqual(expected, actual)
