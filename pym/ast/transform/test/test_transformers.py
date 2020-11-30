"""Test the Pym Transformers"""


from unittest import TestCase


from pym.ast.transform.transformers import PymTransformer
from pym.render import render


class PymTransformerTest(TestCase):
    def test_transformer(self):
        expected = render.parse("i = 0\nj = i = 1")
        transformer = PymTransformer()
        actual = transformer.visit(expected)
        self.assertEqual(expected, actual)

    def test_pass_removal(self):
        class PassRemover(PymTransformer):
            def visit_Pass(self, _node):
                # pylint: disable-msg=no-self-use
                return None

        transformer = PassRemover()
        ast = render.parse("pass")
        ast = transformer.visit(ast)
        actual = render.render(ast)
        self.assertEqual("", actual)

    def test_string_emptying(self):
        class StringBlanker(PymTransformer):
            def visit_Str(self, _node):
                # pylint: disable-msg=no-self-use
                return "pass"

        transformer = StringBlanker()
        ast = render.parse('"contents"')
        ast = transformer.visit(ast)
        actual = render.render(ast)
        self.assertEqual("pass", actual)

    def test_string_removal_from_module(self):
        class StringBlanker(PymTransformer):
            def visit_Expr(self, _node):
                # pylint: disable-msg=no-self-use
                return None

        transformer = StringBlanker()
        ast = render.parse('"contents"')
        ast = transformer.visit(ast)
        actual = render.render(ast)
        self.assertEqual("", actual)

    def test_string_removal_from_expression(self):
        class StringBlanker(PymTransformer):
            def visit_Expr(self, _node):
                # pylint: disable-msg=no-self-use
                return None

        transformer = StringBlanker()
        ast = render.parse('i=0\n"contents"')
        ast = transformer.visit(ast)
        actual = render.render(ast)
        self.assertEqual("i = 0", actual)
