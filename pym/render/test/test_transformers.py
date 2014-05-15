"""Test the Pym Transformers"""


from unittest import TestCase


from pym.render.transformers import PymTransformer
from pym.render import render


class MockTransformer(PymTransformer):
    def visit_Assign(self, node):
        # pylint: disable-msg=no-self-use
        if node.lineno == 2:
            return None
        return node


class PymTransformerTest(TestCase):

    def setUp(self):
        self.ast = render.parse('i = 0\nj = i = 1')

    def test_transformer(self):
        expected = self.ast
        transformer = PymTransformer()
        actual = transformer.visit(expected)
        self.assertEqual(expected, actual)

    def test_removal(self):
        transformer = MockTransformer()
        ast = transformer.visit(self.ast)
        actual = render.render(ast)
        self.assertNotIn('i = 1', actual)
