"""Test that lines are added to a module AST"""


from unittest import TestCase


from pym.ast.parse import parse
from pym.ast.transform.reliner import Liner, adjust_lines
from pym.render.render import render
from pym.ast.transform.docstringer import recast_docstrings


def re_render(module_text):
    tree = parse(module_text)
    recast_docstrings(tree)
    adjust_lines(tree)
    return render(tree)


class TestLineariness(TestCase):

    def test_initialisation(self):
        self.assertIsNotNone(Liner())

    def test_add_no_lines_to_nothing(self):
        actual = re_render('')
        self.assertEqual('', actual)

    def test_add_no_lines_to_docstring(self):
        expected = '"""This is a docstring"""'
        actual = re_render(expected)
        self.assertEqual(expected, actual)

    def test_add_blank_lines(self):
        expected = '''"""This is a docstring"""


import os
import sys
from pprint import pprint
from mine import yours


def method():
    pass


def another():
    pass


class Thing(object):
    pass


result = os.EX_OK
method = another


def main():
    return result


result = not os.EX_OK
if __name__ == '__main__':
    sys.exit(main())'''
        actual = re_render(expected)
        self.assertEqual(expected, actual)
