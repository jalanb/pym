"""Test that sections are added to a module AST"""


from unittest import TestCase


from pym.ast.parse import parse
from pym.ast.transform.module_sectioner import Sectioner, add_sections
from pym.render.render import render
from pym.ast.transform.docstringer import recast_docstrings


def re_render(module_text):
    tree = parse(module_text)
    recast_docstrings(tree)
    add_sections(tree)
    return render(tree)


class TestSectioner(TestCase):

    def test_initialisation(self):
        transformer = Sectioner()
        self.assertIsNotNone(transformer)

    def test_add_no_sections_to_nothing(self):
        actual = re_render('')
        self.assertEqual('', actual)

    def test_add_no_sections_to_docstring(self):
        expected = '"""This is a docstring"""'
        actual = re_render(expected)
        self.assertEqual(expected, actual)

    def test_add_blank_lines(self):
        expected = '''"""This is a docstring"""


import os'''
        actual = re_render(expected)
        self.assertEqual(expected, actual)
